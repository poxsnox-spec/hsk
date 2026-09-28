#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Патч server.py — API для Business уроков + маршруты."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "web" / "server.py"

# Вставляем перед /static
ROUTES = '''

# ============================================================
# Business Chinese
# ============================================================
BIZ_DIR = DATA / "business"

@app.route("/business/lesson/<int:n>")
def business_lesson_page(n):
    """Страница бизнес-урока."""
    return send_from_directory(str(STATIC), "business_lesson.html")

@app.route("/api/business/lessons")
def api_business_lessons():
    """Список всех бизнес-уроков (только шапки)."""
    if not BIZ_DIR.exists():
        return jsonify([])
    out = []
    for f in sorted(BIZ_DIR.glob("lesson*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        out.append({
            "lesson": d.get("lesson"),
            "module": d.get("module"),
            "title": d.get("title", {}),
            "module_title": d.get("module_title", {}),
            "status": d.get("status", "full"),
        })
    return jsonify(out)

@app.route("/api/business/lessons/<int:n>")
def api_business_lesson(n):
    """Полные данные урока."""
    f = BIZ_DIR / f"lesson{n:02d}.json"
    if not f.exists():
        return jsonify({"error": "not found"}), 404
    try:
        return jsonify(json.loads(f.read_text(encoding="utf-8")))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''

def main():
    src = SERVER.read_text(encoding="utf-8")
    if "/api/business/lessons" in src:
        print("Уже пропатчено")
        return
    marker = '@app.route("/static/'
    if marker not in src:
        print("!! не нашёл @app.route(\"/static/"); sys.exit(1)
    src = src.replace(marker, ROUTES + marker, 1)
    if src.count("{") != src.count("}"):
        print("!! баланс скобок нарушен, не пишу"); sys.exit(1)
    shutil.copy2(SERVER, SERVER.with_suffix(SERVER.suffix + ".pre_biz_api.bak"))
    SERVER.write_text(src, encoding="utf-8")
    print("OK: server.py — /business/lesson/<n>, /api/business/lessons")
    print("Бэкап: server.py.pre_biz_api.bak")

if __name__ == "__main__":
    main()