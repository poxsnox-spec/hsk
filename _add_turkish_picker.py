#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет турецкий (tr) в массив LANGS поп-апa в web/static/index.html."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "web" / "static" / "index.html"


def main():
    src = INDEX.read_text(encoding="utf-8")

    pattern = re.compile(
        r'(var\s+LANGS\s*=\s*\[)(.*?)(\];)',
        re.DOTALL,
    )
    m = pattern.search(src)
    if not m:
        print("!! не нашёл var LANGS в index.html")
        return

    inner = m.group(2)
    if 'code: "tr"' in inner or "code: 'tr'" in inner:
        print("tr уже есть в LANGS — ничего не делаю")
        return

    # Убедимся, что после последней записи есть запятая
    inner_stripped = inner.rstrip()
    if not inner_stripped.endswith(","):
        inner_stripped += ","
    inner_stripped += '\n    { code: "tr", name: "Türkçe"   }\n  '

    new_src = src[:m.start(2)] + inner_stripped + src[m.end(2):]

    bak = INDEX.with_suffix(INDEX.suffix + ".pre_tr.bak")
    shutil.copy2(INDEX, bak)
    INDEX.write_text(new_src, encoding="utf-8")

    print(f"OK: добавлен tr в LANGS. Бэкап: {bak.name}")
    print("Дальше: перезапусти сервер и обнови страницу (Ctrl+Shift+R)")


if __name__ == "__main__":
    main()