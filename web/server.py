# -*- coding: utf-8 -*-
"""Flask-сервер для веб-версии HSK 5 Learner."""
import json
import logging
import os
from pathlib import Path

from flask import (Flask, send_from_directory, jsonify, request,
                   session, redirect)

import auth

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DATA = ROOT / "data" / "lessons"
AUDIO = ROOT / "data" / "audio"
STATIC = BASE / "static"

app = Flask(__name__, static_folder=str(STATIC), static_url_path="/static")
app.secret_key = auth.get_or_create_secret()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,   # True на HTTPS
    PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 30,  # 30 дней
)


# ============================================================
# Почта через Brevo
# ============================================================
BREVO_KEY  = os.environ.get("BREVO_KEY", "")
FROM_EMAIL = "poxsnox@gmail.com"
FROM_NAME  = "HSK5 Learner"


def send_brevo(subject, text, to_email=None, html=None, reply_to=None):
    if not BREVO_KEY:
        print("[mail] BREVO_KEY не задан")
        return False
    try:
        import requests
        payload = {
            "sender": {"email": FROM_EMAIL, "name": FROM_NAME},
            "to": [{"email": to_email or FROM_EMAIL}],
            "subject": subject,
            "textContent": text,
        }
        if html:
            payload["htmlContent"] = html
        if reply_to:
            payload["replyTo"] = {"email": reply_to}
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"accept": "application/json", "api-key": BREVO_KEY,
                     "content-type": "application/json"},
            json=payload, timeout=15,
        )
        if r.status_code in (200, 201, 202):
            return True
        print(f"[mail] Brevo {r.status_code}: {r.text[:200]}")
        return False
    except Exception as e:
        print(f"[mail] Ошибка Brevo: {e}")
        return False


class BrevoHandler(logging.Handler):
    def emit(self, record):
        try:
            send_brevo("[HSK5] Ошибка на сайте", self.format(record))
        except Exception:
            pass


if not app.debug:
    h = BrevoHandler()
    h.setLevel(logging.ERROR)
    h.setFormatter(logging.Formatter(
        "Время: %(asctime)s\nПуть: %(pathname)s:%(lineno)d\nСообщение: %(message)s\n"
    ))
    app.logger.addHandler(h)


# ============================================================
# Хелперы
# ============================================================
def _iter_lessons():
    if not DATA.exists():
        return
    for unit_dir in sorted(DATA.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit"):
            continue
        try:
            unit_num = int(unit_dir.name.replace("unit", ""))
        except ValueError:
            continue
        for lesson_file in sorted(unit_dir.glob("lesson*.json")):
            try:
                lesson_num = int(lesson_file.stem.replace("lesson", ""))
            except ValueError:
                continue
            try:
                data = json.loads(lesson_file.read_text(encoding="utf-8"))
            except Exception:
                continue
            yield unit_num, lesson_num, data


def current_user():
    uid = session.get("uid")
    if not uid:
        return None
    return auth.get_user(uid)


def require_login(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*a, **kw):
        if not session.get("uid"):
            return jsonify({"error": "unauthorized"}), 401
        return fn(*a, **kw)
    return wrapper


def _activation_email(name, link):
    subject = "HSK 5 Learner — подтвердите email"
    text = (
        f"Здравствуйте, {name}!\n\n"
        f"Для активации аккаунта перейдите по ссылке:\n{link}\n\n"
        f"Ссылка действует 24 часа.\n\n"
        f"— HSK 5 Learner"
    )
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;
                padding:28px;background:#0e1620;color:#F0F4F8;border-radius:14px">
      <h2 style="color:#66B2FF;margin:0 0 8px">HSK 5 Learner</h2>
      <p style="color:#8B9AAB;font-size:13px;margin:0 0 24px">
        Подтверждение email</p>
      <p>Здравствуйте, <b>{name}</b>!</p>
      <p>Нажмите кнопку, чтобы активировать аккаунт:</p>
      <p style="margin:26px 0">
        <a href="{link}"
           style="display:inline-block;padding:14px 28px;background:#4a9eff;
                  color:#fff;text-decoration:none;border-radius:10px;
                  font-weight:600">
          Активировать аккаунт
        </a>
      </p>
      <p style="font-size:13px;color:#8B9AAB">
        Ссылка действует 24 часа. Если кнопка не работает, скопируйте ссылку:<br>
        <span style="color:#66B2FF;word-break:break-all">{link}</span>
      </p>
    </div>"""
    return subject, text, html


# ============================================================
# Статика / аудио
# ============================================================
@app.route("/")
def index():
    return send_from_directory(str(STATIC), "index.html")


@app.route("/static/<path:fname>")
def static_files(fname):
    return send_from_directory(str(STATIC), fname)


@app.route("/audio/<path:fname>")
def audio_files(fname):
    if not AUDIO.exists():
        return jsonify({"error": "audio dir missing"}), 404
    return send_from_directory(str(AUDIO), fname)


# ============================================================
# AUTH
# ============================================================
@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    d = request.get_json(silent=True) or {}
    res = auth.register(d.get("name"), d.get("email"), d.get("password"))
    if not res["ok"]:
        return jsonify({"error": res["error"]}), 400

    # для админа — сразу логиним
    if res["user"]["is_admin"]:
        session.permanent = True
        session["uid"] = res["user"]["id"]
        return jsonify({"ok": True, "user": res["user"], "is_admin": True})

    # шлём письмо
    link = f"{request.host_url.rstrip('/')}/#activate/{res['token']}"
    subj, text, html = _activation_email(res["user"]["name"], link)
    send_brevo(subj, text, to_email=res["user"]["email"], html=html)
    return jsonify({
        "ok": True,
        "need_activation": True,
        "email": res["user"]["email"],
    })


@app.route("/api/auth/activate/<token>")
def auth_activate(token):
    res = auth.activate(token)
    if not res["ok"]:
        return jsonify({"error": res["error"]}), 400
    session.permanent = True
    session["uid"] = res["user"]["id"]
    return jsonify({"ok": True, "user": res["user"]})


@app.route("/api/auth/resend", methods=["POST"])
def auth_resend():
    d = request.get_json(silent=True) or {}
    res = auth.resend_activation(d.get("email"))
    if not res["ok"]:
        return jsonify({"error": res["error"]}), 400
    link = f"{request.host_url.rstrip('/')}/#activate/{res['token']}"
    subj, text, html = _activation_email(res["name"], link)
    send_brevo(subj, text, to_email=res["email"], html=html)
    return jsonify({"ok": True})


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    d = request.get_json(silent=True) or {}
    res = auth.login(d.get("email"), d.get("password"))
    if not res["ok"]:
        return jsonify(res), 400
    session.permanent = True
    session["uid"] = res["user"]["id"]
    return jsonify({"ok": True, "user": res["user"]})


@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/auth/me")
def auth_me():
    u = current_user()
    if not u:
        return jsonify({"user": None})
    return jsonify({"user": u})


# ============================================================
# PROGRESS
# ============================================================
@app.route("/api/progress", methods=["GET"])
@require_login
def progress_all():
    return jsonify(auth.progress_get_all(session["uid"]))


@app.route("/api/progress/<key>", methods=["PUT"])
@require_login
def progress_put(key):
    body = request.get_json(silent=True) or {}
    ok = auth.progress_set(session["uid"], key, body.get("value"))
    if not ok:
        return jsonify({"error": "bad data"}), 400
    return jsonify({"ok": True})


@app.route("/api/progress", methods=["DELETE"])
@require_login
def progress_reset():
    n = auth.progress_reset(session["uid"])
    return jsonify({"ok": True, "deleted": n})


# ============================================================
# Уроки / слова / грамматика (публичные, но можно требовать логин)
# ============================================================
@app.route("/api/lessons")
@require_login
def api_lessons_list():
    out = []
    for u, l, data in _iter_lessons():
        out.append({"unit": u, "lesson": l, "title": data.get("title", {})})
    return jsonify(out)


@app.route("/api/lessons/<int:unit>/<int:lesson>")
@require_login
def api_lesson(unit, lesson):
    path = DATA / f"unit{unit}" / f"lesson{lesson:02d}.json"
    if not path.exists():
        return jsonify({"error": "not found"}), 404
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        app.logger.exception("Не удалось прочитать JSON")
        return jsonify({"error": str(e)}), 500
    return jsonify(data)


@app.route("/api/vocab")
@require_login
def api_vocab():
    out = []
    for u, l, data in _iter_lessons():
        for w in data.get("vocabulary", []) or []:
            if not isinstance(w, dict):
                continue
            out.append({
                "hanzi": w.get("hanzi", ""),
                "pinyin": w.get("pinyin", ""),
                "pos": w.get("pos", ""),
                "meaning": w.get("meaning", {}) or {},
                "unit": u, "lesson": l,
            })
    return jsonify(out)


@app.route("/api/grammar")
@require_login
def api_grammar():
    out = []
    for u, l, data in _iter_lessons():
        for g in data.get("grammar", []) or []:
            if not isinstance(g, dict):
                continue
            out.append({
                "word": g.get("word", ""),
                "pos": g.get("pos", ""),
                "explanation": g.get("explanation", {}) or {},
                "examples": g.get("examples", []) or [],
                "unit": u, "lesson": l,
            })
    return jsonify(out)


@app.route("/api/compare")
@require_login
def api_compare():
    out = []
    for u, l, data in _iter_lessons():
        for cp in data.get("comparisons", []) or []:
            if not isinstance(cp, dict):
                continue
            out.append({
                "word_a": cp.get("word_a", ""),
                "word_b": cp.get("word_b", ""),
                "common": cp.get("common", {}) or {},
                "differences": cp.get("differences", []) or [],
                "unit": u, "lesson": l,
            })
    return jsonify(out)


# ============================================================
# Обратная связь
# ============================================================
@app.route("/api/feedback", methods=["POST"])
@require_login
def api_feedback():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()[:80]
    message = (data.get("message") or "").strip()[:3000]
    if not message:
        return jsonify({"error": "empty"}), 400
    u = current_user()
    body = (
        f"От: {name or u['name']}\n"
        f"Email: {u['email']}\n\n{message}"
    )
    ok = send_brevo("[HSK5] Сообщение от друга", body)
    return jsonify({"ok": ok}), (200 if ok else 500)


# ============================================================
# ADMIN
# ============================================================
@app.route("/api/admin/users")
@require_login
def admin_users():
    u = current_user()
    if not u or not u["is_admin"]:
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"users": auth.list_users()})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("Запуск на http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)