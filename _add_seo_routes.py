#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет /sitemap.xml и /robots.txt в web/server.py."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "web" / "server.py"

ROUTES = '''

@app.route("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(str(STATIC), "sitemap.xml", mimetype="application/xml")


@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(str(STATIC), "robots.txt", mimetype="text/plain")

'''


def main():
    src = SERVER.read_text(encoding="utf-8")
    if 'def sitemap_xml' in src:
        print("server.py уже пропатчен")
        return
    marker = 'if __name__ == "__main__":'
    if marker not in src:
        print("!! не нашёл if __name__ в server.py")
        return
    src = src.replace(marker, ROUTES + marker, 1)
    bak = SERVER.with_suffix(SERVER.suffix + ".pre_seo.bak")
    shutil.copy2(SERVER, bak)
    SERVER.write_text(src, encoding="utf-8")
    print("OK: server.py пропатчен. Бэкап:", bak.name)
    print("Дальше: git add + commit + push → на сервере git pull + Reload")


if __name__ == "__main__":
    main()