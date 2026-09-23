# -*- coding: utf-8 -*-
"""Аутентификация, регистрация, активация, прогресс, профиль, сброс пароля."""
import json
import secrets
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from werkzeug.security import generate_password_hash, check_password_hash

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
DB_FILE = DATA / "users.db"
SECRET_FILE = DATA / "secret.key"

ADMIN_EMAIL = "poxsnox@gmail.com"
ACTIVATION_HOURS = 24
RESET_HOURS = 1


def get_or_create_secret() -> str:
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text(encoding="utf-8").strip()
    key = secrets.token_hex(32)
    SECRET_FILE.write_text(key, encoding="utf-8")
    return key


def _conn():
    c = sqlite3.connect(DB_FILE)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    return c


def init_db():
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                avatar TEXT DEFAULT '👤',
                hsk_level TEXT DEFAULT 'HSK5',
                created_at TEXT NOT NULL,
                activated INTEGER DEFAULT 0,
                activate_token TEXT,
                activate_expires TEXT,
                reset_token TEXT,
                reset_expires TEXT,
                is_admin INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS progress (
                user_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, key),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
        """)
        # миграция: добавить новые колонки, если база старая
        cols = {r["name"] for r in c.execute("PRAGMA table_info(users)").fetchall()}
        for col, typ in (("reset_token", "TEXT"), ("reset_expires", "TEXT"),
                         ("hsk_level", "TEXT")):
            if col not in cols:
                c.execute(f"ALTER TABLE users ADD COLUMN {col} {typ}")
        c.commit()


def _now() -> str:
    return datetime.utcnow().isoformat()


def _user_to_dict(row) -> dict:
    if not row:
        return None
    return {
        "id": row["id"],
        "email": row["email"],
        "name": row["name"],
        "avatar": row["avatar"],
        "hsk_level": row["hsk_level"] if "hsk_level" in row.keys() else "HSK5",
        "created_at": row["created_at"],
        "activated": bool(row["activated"]),
        "is_admin": bool(row["is_admin"]),
    }


# ============================================================
# Регистрация
# ============================================================
def register(name: str, email: str, password: str) -> dict:
    name = (name or "").strip()[:60]
    email = (email or "").strip().lower()
    password = password or ""

    if not name:
        return {"ok": False, "error": "Введите имя"}
    if "@" not in email or "." not in email or len(email) < 5:
        return {"ok": False, "error": "Некорректный email"}
    if len(password) < 6:
        return {"ok": False, "error": "Пароль минимум 6 символов"}

    is_admin = (email == ADMIN_EMAIL.lower())
    token = secrets.token_urlsafe(32)
    expires = (datetime.utcnow() + timedelta(hours=ACTIVATION_HOURS)).isoformat()

    try:
        with _conn() as c:
            c.execute(
                "INSERT INTO users (email, name, password_hash, created_at,"
                " activated, activate_token, activate_expires, is_admin)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (email, name, generate_password_hash(password),
                 _now(), 1 if is_admin else 0, token, expires,
                 1 if is_admin else 0),
            )
            c.commit()
            row = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    except sqlite3.IntegrityError:
        return {"ok": False, "error": "Этот email уже зарегистрирован"}

    return {
        "ok": True,
        "user": _user_to_dict(row),
        "token": token,
        "need_activation": not is_admin,
        "is_admin": is_admin,
    }


# ============================================================
# Активация
# ============================================================
def activate(token: str) -> dict:
    if not token:
        return {"ok": False, "error": "Токен отсутствует"}
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE activate_token = ?", (token,)).fetchone()
        if not row:
            return {"ok": False, "error": "Неверная ссылка активации"}
        if row["activated"]:
            return {"ok": True, "user": _user_to_dict(row), "already": True}
        try:
            exp = datetime.fromisoformat(row["activate_expires"])
            if datetime.utcnow() > exp:
                return {"ok": False, "error": "Срок ссылки истёк. Запросите новую."}
        except Exception:
            pass
        c.execute(
            "UPDATE users SET activated = 1, activate_token = NULL,"
            " activate_expires = NULL WHERE id = ?",
            (row["id"],),
        )
        c.commit()
        row = c.execute("SELECT * FROM users WHERE id = ?", (row["id"],)).fetchone()
    return {"ok": True, "user": _user_to_dict(row)}


def resend_activation(email: str) -> dict:
    email = (email or "").strip().lower()
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not row:
            return {"ok": False, "error": "Email не найден"}
        if row["activated"]:
            return {"ok": False, "error": "Аккаунт уже активирован"}
        token = secrets.token_urlsafe(32)
        expires = (datetime.utcnow() + timedelta(hours=ACTIVATION_HOURS)).isoformat()
        c.execute(
            "UPDATE users SET activate_token = ?, activate_expires = ? WHERE id = ?",
            (token, expires, row["id"]),
        )
        c.commit()
    return {"ok": True, "token": token, "email": row["email"], "name": row["name"]}


# ============================================================
# Сброс пароля
# ============================================================
def create_reset_token(email: str) -> dict:
    email = (email or "").strip().lower()
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not row:
            return {"ok": False, "error": "Email не найден"}
        if not row["activated"]:
            return {"ok": False, "error": "Аккаунт ещё не активирован"}
        token = secrets.token_urlsafe(32)
        expires = (datetime.utcnow() + timedelta(hours=RESET_HOURS)).isoformat()
        c.execute(
            "UPDATE users SET reset_token = ?, reset_expires = ? WHERE id = ?",
            (token, expires, row["id"]),
        )
        c.commit()
    return {"ok": True, "token": token, "email": row["email"], "name": row["name"]}


def reset_password(token: str, new_password: str) -> dict:
    if not token:
        return {"ok": False, "error": "Токен отсутствует"}
    if not new_password or len(new_password) < 6:
        return {"ok": False, "error": "Пароль минимум 6 символов"}
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE reset_token = ?", (token,)).fetchone()
        if not row:
            return {"ok": False, "error": "Неверная ссылка"}
        try:
            exp = datetime.fromisoformat(row["reset_expires"])
            if datetime.utcnow() > exp:
                return {"ok": False, "error": "Срок ссылки истёк. Запросите новую."}
        except Exception:
            pass
        c.execute(
            "UPDATE users SET password_hash = ?, reset_token = NULL,"
            " reset_expires = NULL WHERE id = ?",
            (generate_password_hash(new_password), row["id"]),
        )
        c.commit()
        row2 = c.execute("SELECT * FROM users WHERE id = ?", (row["id"],)).fetchone()
    return {"ok": True, "user": _user_to_dict(row2)}


# ============================================================
# Логин
# ============================================================
def login(email: str, password: str) -> dict:
    email = (email or "").strip().lower()
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if not row or not check_password_hash(row["password_hash"], password or ""):
        return {"ok": False, "error": "Неверный email или пароль"}
    if not row["activated"]:
        return {"ok": False, "error": "Аккаунт не активирован",
                "need_activation": True, "email": email}
    return {"ok": True, "user": _user_to_dict(row)}


def get_user(user_id: int):
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return _user_to_dict(row)


# ============================================================
# Профиль
# ============================================================
def update_profile(user_id: int, name=None, avatar=None) -> dict:
    with _conn() as c:
        if name is not None:
            n = (name or "").strip()[:60]
            if not n:
                return {"ok": False, "error": "Имя не может быть пустым"}
            c.execute("UPDATE users SET name = ? WHERE id = ?", (n, user_id))
        if avatar is not None:
            a = (avatar or "").strip()[:8]
            if a:
                c.execute("UPDATE users SET avatar = ? WHERE id = ?", (a, user_id))
        c.commit()
        row = c.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return {"ok": True, "user": _user_to_dict(row)}


# ============================================================
# Прогресс
# ============================================================
def progress_get_all(user_id: int) -> dict:
    with _conn() as c:
        rows = c.execute(
            "SELECT key, value FROM progress WHERE user_id = ?", (user_id,)
        ).fetchall()
    return {r["key"]: _safe_json(r["value"]) for r in rows}


def progress_set(user_id: int, key: str, value) -> bool:
    if not key or len(key) > 100:
        return False
    try:
        raw = json.dumps(value, ensure_ascii=False)
    except Exception:
        return False
    if len(raw) > 200_000:
        return False
    with _conn() as c:
        c.execute(
            "INSERT INTO progress (user_id, key, value, updated_at)"
            " VALUES (?, ?, ?, ?)"
            " ON CONFLICT(user_id, key) DO UPDATE"
            " SET value = excluded.value, updated_at = excluded.updated_at",
            (user_id, key, raw, _now()),
        )
        c.commit()
    return True


def progress_reset(user_id: int) -> int:
    with _conn() as c:
        cur = c.execute("DELETE FROM progress WHERE user_id = ?", (user_id,))
        c.commit()
        return cur.rowcount


def _safe_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return s


# ============================================================
# Админ
# ============================================================
def list_users() -> list:
    with _conn() as c:
        rows = c.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    out = []
    for r in rows:
        with _conn() as c2:
            cnt = c2.execute(
                "SELECT COUNT(*) AS n FROM progress WHERE user_id = ?", (r["id"],)
            ).fetchone()["n"]
            last = c2.execute(
                "SELECT MAX(updated_at) AS m FROM progress WHERE user_id = ?", (r["id"],)
            ).fetchone()["m"]
        d = _user_to_dict(r)
        d["progress_keys"] = cnt
        d["last_seen"] = last
        out.append(d)
    return out


def get_user_progress_summary(user_id: int) -> dict:
    """Сводка прогресса для админки."""
    with _conn() as c:
        rows = c.execute(
            "SELECT key, value, updated_at FROM progress WHERE user_id = ?",
            (user_id,),
        ).fetchall()
    raw = {}
    for r in rows:
        raw[r["key"]] = _safe_json(r["value"])
    # вытащим сводку из известных ключей
    lessons = raw.get("hsk5_lessons_opened", []) or []
    srs = raw.get("hsk5_srs", {}) or {}
    activity = raw.get("hsk5_activity", {}) or {}
    actions = sum(activity.values()) if isinstance(activity, dict) else 0
    return {
        "lessons_count": len(lessons),
        "srs_words": len(srs),
        "actions_total": actions,
        "activity_days": len([v for v in activity.values() if v > 0]) if isinstance(activity, dict) else 0,
        "raw_keys": list(raw.keys()),
        "activity": activity,
    }


def delete_user(user_id: int) -> dict:
    with _conn() as c:
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        c.commit()
    return {"ok": True}


init_db()