#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет HSK6-модуль в проект: роут в server.py + угловая кнопка в app.js."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
SERVER = WEB / "server.py"
APP = WEB / "static" / "app.js"

ROUTE = '''

# ============================================================
# HSK 6 module
# ============================================================
try:
    import hsk6
    hsk6.register(app)
except Exception as _e:
    print("[hsk6] не удалось подключить:", _e)

'''

CORNER = '''

// === HSK6: угловая кнопка ===
(function hsk6CornerInit(){
  if (document.getElementById("hsk6-corner-style")) return;
  const st = document.createElement("style");
  st.id = "hsk6-corner-style";
  st.textContent = `
    #hsk6-corner-btn {
      position: fixed; top: 14px; right: 84px; z-index: 900;
      display: flex; align-items: center; gap: 6px;
      padding: 8px 12px 8px 10px; border-radius: 12px;
      background: linear-gradient(135deg, #a63a2a, #c8624f);
      color: #f5f0e6; font-size: 13px; font-weight: 600;
      cursor: pointer; border: 0;
      box-shadow: 0 6px 18px rgba(166,58,42,0.35);
      transition: transform .15s ease, box-shadow .15s ease;
      text-decoration: none; font-family: inherit;
    }
    #hsk6-corner-btn:hover { transform: translateY(-2px); }
    @media (max-width: 640px) {
      #hsk6-corner-btn .lbl { display: none; }
      #hsk6-corner-btn { padding: 9px; border-radius: 50%; width: 40px; height: 40px; justify-content: center; right: 70px; }
    }
  `;
  document.head.appendChild(st);
  function mount() {
    if (document.getElementById("hsk6-corner-btn")) return;
    const a = document.createElement("a");
    a.id = "hsk6-corner-btn";
    a.href = "/hsk6";
    a.title = "HSK 6 · 2500 词";
    a.innerHTML = '<span>中文</span><span class="lbl">HSK 6</span>';
    document.body.appendChild(a);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
'''


def patch_server():
    src = SERVER.read_text(encoding="utf-8")
    if "hsk6.register(app)" in src:
        print("server.py уже пропатчен")
        return
    marker = 'if __name__ == "__main__":'
    if marker not in src:
        print("!! не нашёл if __name__ в server.py")
        return
    src = src.replace(marker, ROUTE + marker, 1)
    bak = SERVER.with_suffix(SERVER.suffix + ".pre_hsk6.bak")
    shutil.copy2(SERVER, bak)
    SERVER.write_text(src, encoding="utf-8")
    print("OK: server.py пропатчен. Бэкап:", bak.name)


def patch_app():
    if not APP.exists():
        print("!! нет web/static/app.js")
        return
    src = APP.read_text(encoding="utf-8")
    if "hsk6-corner-btn" in src:
        print("app.js уже пропатчен")
        return
    bak = APP.with_suffix(APP.suffix + ".pre_hsk6.bak")
    shutil.copy2(APP, bak)
    APP.write_text(src + CORNER, encoding="utf-8")
    print("OK: app.js пропатчен. Бэкап:", bak.name)


def main():
    print("=" * 60)
    print("ДОБАВЛЕНИЕ HSK6")
    print("=" * 60)
    patch_server()
    patch_app()
    print()
    print("ГОТОВО. Дальше:")
    print("  set DEEPSEEK_API_KEY=sk-...")
    print("  python web\\server.py")
    print("  Открыть http://127.0.0.1:5000/hsk6")


if __name__ == "__main__":
    main()