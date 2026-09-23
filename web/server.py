# -*- coding: utf-8 -*-
"""Flask-сервер для веб-версии HSK 5 Learner."""
import json
import logging
import os
from pathlib import Path
from flask import Flask, send_from_directory, jsonify, request

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DATA = ROOT / "data" / "lessons"
AUDIO = ROOT / "data" / "audio"
STATIC = BASE / "static"

app = Flask(__name__, static_folder=str(STATIC), static_url_path="/static")


# ============================================================
# Почта через Brevo
# ============================================================
BREVO_KEY  = os.environ.get("BREVO_KEY", "")
FROM_EMAIL = "poxsnox@gmail.com"
TO_EMAIL   = "poxsnox@gmail.com"
FROM_NAME  = "HSK5 Learner"


def send_brevo(subject, text, reply_to=None):
    if not BREVO_KEY:
        print("[mail] BREVO_KEY не задан")
        return False
    try:
        import requests
        payload = {
            "sender": {"email": FROM_EMAIL, "name": FROM_NAME},
            "to": [{"email": TO_EMAIL}],
            "subject": subject,
            "textContent": text,
        }
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
# Хелпер: обход уроков
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


# ============================================================
# Маршруты
# ============================================================
@app.route("/")
def index():
    return send_from_directory(str(STATIC), "index.html")


@app.route("/static/<path:fname>")
def static_files(fname):
    return send_from_directory(str(STATIC), fname)


# ---- АУДИО ----
@app.route("/audio/<path:fname>")
def audio_files(fname):
    """Отдаёт mp3 из data/audio/."""
    if not AUDIO.exists():
        return jsonify({"error": "audio dir missing"}), 404
    return send_from_directory(str(AUDIO), fname)


@app.route("/api/lessons")
def api_lessons_list():
    out = []
    for u, l, data in _iter_lessons():
        out.append({"unit": u, "lesson": l, "title": data.get("title", {})})
    return jsonify(out)


@app.route("/api/lessons/<int:unit>/<int:lesson>")
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


@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()[:80]
    message = (data.get("message") or "").strip()[:3000]
    if not message:
        return jsonify({"error": "empty"}), 400
    body = f"От: {name or 'аноним'}\n\n{message}"
    ok = send_brevo("[HSK5] Сообщение от друга", body)
    return jsonify({"ok": ok}), (200 if ok else 500)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("Запуск на http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)