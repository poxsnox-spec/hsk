#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Вставляет Google Analytics 4 тег во все HTML-файлы в web/static/."""
import re
from pathlib import Path

GA_ID = "G-6882T6HG4V"

TAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '%s');
</script>
''' % (GA_ID, GA_ID)


def patch_html(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    if GA_ID in src:
        print(f"  skip (already has tag): {path.name}")
        return False
    m = re.search(r"<head[^>]*>", src, re.IGNORECASE)
    if not m:
        print(f"  no <head>: {path.name}")
        return False
    new = src[:m.end()] + "\n" + TAG + src[m.end():]
    path.write_text(new, encoding="utf-8")
    print(f"  ok: {path.name}")
    return True


def main():
    static = Path(__file__).resolve().parent / "web" / "static"
    files = sorted(static.glob("*.html"))
    print(f"Найдено {len(files)} HTML-файлов")
    changed = 0
    for f in files:
        if patch_html(f):
            changed += 1
    print(f"\nГотово. Обновлено: {changed}")
    print("Дальше: git add + commit + push → на PythonAnywhere git pull + Reload")


if __name__ == "__main__":
    main()