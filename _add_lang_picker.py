#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет showLangPicker popup + обновляет cycleLang и langName (7 языков)."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "web" / "static" / "app.js"

# ---------- 1) Обновлённые langName и cycleLang ----------
NEW_LANGNAME = '''function langName() {
  return {
    ru: "Сменить язык",
    en: "Change language",
    tk: "Dili çalyş",
    uz: "Tilni o'zgartirish",
    tg: "Иваз кардани забон",
    id: "Ganti bahasa",
    tr: "Dili değiştir",
  }[getLang()] || "Change language";
}
'''

NEW_CYCLELANG = '''function cycleLang() {
  const o = ["ru", "en", "tk", "uz", "tg", "id", "tr"];
  const c = getLang();
  setLang(o[(o.indexOf(c) + 1) % o.length]);
}
'''

# ---------- 2) Popup showLangPicker ----------
POPUP_CODE = r'''

// ============================================================
// Language picker popup (7 языков)
// ============================================================
window.showLangPicker = function(force){
  if (document.getElementById("lp-overlay")) return;

  const LANGS = [
    { code: "ru", flag: "🇷🇺", name: "Русский" },
    { code: "en", flag: "🇬🇧", name: "English" },
    { code: "tk", flag: "🇹🇲", name: "Türkmen" },
    { code: "uz", flag: "🇺🇿", name: "O'zbek" },
    { code: "tg", flag: "🇹🇯", name: "Тоҷикӣ" },
    { code: "id", flag: "🇮🇩", name: "Indonesia" },
    { code: "tr", flag: "🇹🇷", name: "Türkçe" },
  ];
  const current = (typeof getLang === "function") ? getLang() : "ru";

  const titles = {
    ru: "Язык интерфейса",
    en: "Interface language",
    tk: "Interfeýs dili",
    uz: "Interfeys tili",
    tg: "Забони интерфейс",
    id: "Bahasa antarmuka",
    tr: "Arayüz dili",
  };
  const subtitles = {
    ru: "Выберите язык",
    en: "Choose a language",
    tk: "Dil saýlaň",
    uz: "Tilni tanlang",
    tg: "Забонро интихоб кунед",
    id: "Pilih bahasa",
    tr: "Bir dil seçin",
  };

  const overlay = document.createElement("div");
  overlay.id = "lp-overlay";
  overlay.style.cssText = `
    position: fixed; inset: 0;
    background: rgba(8, 12, 20, 0.75);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    z-index: 9999;
    display: flex; align-items: center; justify-content: center;
    padding: 20px;
    animation: lpFadeIn .2s ease;
  `;

  const style = document.createElement("style");
  style.textContent = `
    @keyframes lpFadeIn { from { opacity: 0 } to { opacity: 1 } }
    @keyframes lpSlideUp { from { opacity: 0; transform: translateY(20px) scale(.97) } to { opacity: 1; transform: translateY(0) scale(1) } }
    #lp-card {
      background: linear-gradient(160deg, #1b2333 0%, #141a26 100%);
      border: 1px solid #2a3446;
      border-radius: 18px;
      padding: 26px 24px 20px;
      width: 100%; max-width: 420px;
      box-shadow: 0 24px 60px rgba(0,0,0,.55);
      color: #E6EDF5;
      animation: lpSlideUp .3s cubic-bezier(.2,.8,.2,1);
      font-family: 'Inter', -apple-system, sans-serif;
    }
    #lp-card h2 {
      font-size: 20px; font-weight: 700; margin: 0 0 4px;
    }
    #lp-card p {
      font-size: 13px; color: #8B9AAB; margin: 0 0 18px;
    }
    .lp-item {
      display: flex; align-items: center; gap: 14px;
      width: 100%;
      padding: 14px 16px;
      margin-bottom: 8px;
      border-radius: 12px;
      border: 1px solid #2a3446;
      background: rgba(255,255,255,0.02);
      color: #E6EDF5;
      font-family: inherit;
      font-size: 15px;
      cursor: pointer;
      transition: all .15s;
      text-align: left;
    }
    .lp-item:hover {
      background: rgba(102,178,255,0.08);
      border-color: #4a9eff;
      transform: translateX(2px);
    }
    .lp-item.active {
      background: rgba(102,178,255,0.15);
      border-color: #66B2FF;
      font-weight: 600;
    }
    .lp-item .lp-flag { font-size: 24px; line-height: 1; }
    .lp-item .lp-name { flex: 1; }
    .lp-item .lp-code {
      font-size: 11px; color: #6E7A8A;
      text-transform: uppercase; letter-spacing: 0.5px;
      padding: 3px 8px; border-radius: 5px;
      background: rgba(255,255,255,0.04);
    }
    .lp-item.active .lp-code { color: #66B2FF; background: rgba(102,178,255,0.15); }
    #lp-close {
      width: 100%; padding: 12px;
      margin-top: 6px;
      border-radius: 12px;
      border: 1px solid #333;
      background: transparent;
      color: #E6EDF5;
      font-family: inherit;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
    }
    #lp-close:hover { background: rgba(255,255,255,0.04); }
  `;
  overlay.appendChild(style);

  const card = document.createElement("div");
  card.id = "lp-card";
  card.innerHTML = `
    <h2>${titles[current] || titles.en}</h2>
    <p>${subtitles[current] || subtitles.en}</p>
    <div id="lp-list"></div>
    <button id="lp-close">✕</button>
  `;
  overlay.appendChild(card);
  document.body.appendChild(overlay);

  const list = card.querySelector("#lp-list");
  for (const L of LANGS) {
    const b = document.createElement("button");
    b.className = "lp-item" + (L.code === current ? " active" : "");
    b.innerHTML = `
      <span class="lp-flag">${L.flag}</span>
      <span class="lp-name">${L.name}</span>
      <span class="lp-code">${L.code}</span>
    `;
    b.onclick = () => {
      if (typeof setLang === "function") {
        setLang(L.code);
      }
      overlay.remove();
      try {
        if (typeof navigate === "function") {
          navigate(window.location.hash.slice(1) || "menu");
        }
      } catch(e) {}
    };
    list.appendChild(b);
  }

  card.querySelector("#lp-close").onclick = () => overlay.remove();
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.remove();
  });
  document.addEventListener("keydown", function esc(e){
    if (e.key === "Escape") {
      overlay.remove();
      document.removeEventListener("keydown", esc);
    }
  });
};
'''


def replace_function(src: str, func_name: str, new_body: str) -> str:
    """Заменяет function NAME() { ... } на new_body (точное совпадение до закрывающей })."""
    pat = re.compile(
        rf"function\s+{func_name}\s*\(\s*\)\s*\{{.*?\n\}}",
        re.DOTALL,
    )
    m = pat.search(src)
    if not m:
        print(f"  !! не нашёл function {func_name}")
        return src
    return src[:m.start()] + new_body.rstrip("\n") + src[m.end():]


def main():
    src = APP.read_text(encoding="utf-8")
    original = src

    print("[1/3] Обновляю langName…")
    src = replace_function(src, "langName", NEW_LANGNAME)
    print("[2/3] Обновляю cycleLang…")
    src = replace_function(src, "cycleLang", NEW_CYCLELANG)

    print("[3/3] Добавляю showLangPicker popup…")
    if "window.showLangPicker" not in src:
        src = src.rstrip() + "\n" + POPUP_CODE
    else:
        print("  showLangPicker уже есть — пропускаю")

    if src == original:
        print("Ничего не изменилось")
        return

    bak = APP.with_suffix(APP.suffix + ".pre_langpicker.bak")
    shutil.copy2(APP, bak)
    APP.write_text(src, encoding="utf-8")
    print(f"\nOK: app.js обновлён. Бэкап: {bak.name}")
    print("Дальше: Ctrl+C сервер → python web\\server.py → Ctrl+Shift+R в браузере")


if __name__ == "__main__":
    main()