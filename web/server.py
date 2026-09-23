# -*- coding: utf-8 -*-
"""Flask-сервер для веб-версии HSK 5 Learner."""
import json
import logging
from pathlib import Path
from logging.handlers import SMTPHandler
from flask import Flask, send_from_directory, jsonify, request

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DATA = ROOT / "data" / "lessons"
STATIC = BASE / "static"

app = Flask(__name__, static_folder=str(STATIC), static_url_path="/static")


# ============================================================
# Отправка ошибок на email (Gmail)
# ============================================================
MAIL_USERNAME = "poxsnox@gmail.com"
MAIL_PASSWORD = "qcro btjb zwwm uhrv"
MAIL_TO       = "poxsnox@gmail.com"

if not app.debug:
    try:
        mail_handler = SMTPHandler(
            mailhost=("smtp.gmail.com", 587),
            fromaddr=MAIL_USERNAME,
            toaddrs=[MAIL_TO],
            subject="[HSK5] Ошибка в веб-версии",
            credentials=(MAIL_USERNAME, MAIL_PASSWORD),
            secure=(),
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(
            "Время: %(asctime)s\n"
            "Путь: %(pathname)s:%(lineno)d\n"
            "Сообщение: %(message)s\n"
        ))
        app.logger.addHandler(mail_handler)
        print("[mail] Отправка ошибок включена:", MAIL_TO)
    except Exception as e:
        print("[mail] Не удалось настроить отправку ошибок:", e)


# ============================================================
# Маршруты
# ============================================================
@app.route("/")
def index():
    return send_from_directory(str(STATIC), "index.html")


@app.route("/static/<path:fname>")
def static_files(fname):
    return send_from_directory(str(STATIC), fname)


@app.route("/api/lessons")
def api_lessons_list():
    """Список всех уроков с метаданными."""
    out = []
    if not DATA.exists():
        return jsonify(out)
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
                data = {}
            title = data.get("title", {})
            out.append({
                "unit": unit_num,
                "lesson": lesson_num,
                "title": title,
            })
    return jsonify(out)


@app.route("/api/lessons/<int:unit>/<int:lesson>")
def api_lesson(unit, lesson):
    """Полные данные одного урока."""
    path = DATA / f"unit{unit}" / f"lesson{lesson:02d}.json"
    if not path.exists():
        return jsonify({"error": "not found"}), 404
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        app.logger.exception("Не удалось прочитать JSON урока")
        return jsonify({"error": str(e)}), 500
    return jsonify(data)


@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok"})


# ============================================================
# Тестовый маршрут для проверки email
# ============================================================
@app.route("/api/test-error")
def test_error():
    raise RuntimeError("Тестовая ошибка - проверка отправки на почту")


if __name__ == "__main__":
    print("Запуск на http://127.0.0.1:5000")
    print("Ошибки будут приходить на", MAIL_TO)
    app.run(host="0.0.0.0", port=5000, debug=False)