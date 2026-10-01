#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заменяет буквенные бейджи в попапе выбора языка на круглые SVG-флаги."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "web" / "static" / "index.html"

NEW_BLOCK = '''    var FLAG = { en: "gb", ru: "ru", tk: "tm", id: "id", uz: "uz", tg: "tj", tr: "tr" };
    LANGS.forEach(function (L) {
      var b = document.createElement("button");
      b.className = "lang-pick-btn";
      b.type = "button";
      var fc = FLAG[L.code] || L.code;
      b.innerHTML = '<span class="lp-badge" style="display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,255,255,0.18);box-shadow:0 4px 14px rgba(0,0,0,0.35);margin-bottom:10px;background:rgba(255,255,255,0.04)">' +
                    '<img src="https://flagcdn.com/w80/' + fc + '.png" srcset="https://flagcdn.com/w160/' + fc + '.png 2x" alt="' + L.code.toUpperCase() + '" style="width:100%;height:100%;object-fit:cover;display:block">' +
                    '</span>' +
                    '<span class="lp-name">' + L.name + '</span>';
      b.addEventListener("click", function () {
        try { localStorage.setItem("hsk5_lang", L.code); } catch (e) {}
        location.reload();
      });
      grid.appendChild(b);
    });'''

PATTERN = re.compile(
    r"var\s+colors\s*=\s*\{[^}]*\};.*?grid\.appendChild\(b\);\s*\}\);",
    re.DOTALL,
)


def main():
    src = INDEX.read_text(encoding="utf-8")
    if "flagcdn.com" in src:
        print("Уже есть флаги — ничего не делаю")
        return

    m = PATTERN.search(src)
    if not m:
        print("!! Не нашёл блок рендера кружочков. Проверь index.html")
        return

    new_src = src[:m.start()] + NEW_BLOCK + src[m.end():]

    bak = INDEX.with_suffix(INDEX.suffix + ".pre_flags.bak")
    shutil.copy2(INDEX, bak)
    INDEX.write_text(new_src, encoding="utf-8")
    print(f"OK. Флаги добавлены. Бэкап: {bak.name}")
    print("Перезапусти сервер (Ctrl+C → python web\\server.py) и обнови страницу (Ctrl+Shift+R)")


if __name__ == "__main__":
    main()