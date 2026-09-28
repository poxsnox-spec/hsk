#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обновляет What's new баннер:
  - Новая версия (2026-09-28-business)
  - Новые фичи: Business Chinese, 6 languages, audio
  - Свёртывающийся блок «Previous updates» со старым содержимым
"""
import re
import shutil
from pathlib import Path

APP = Path("web/static/app.js")

NEW_VERSION = "2026-09-28-business"

# Полная замена функции wnShowBanner
NEW_BANNER_JS = '''
// ============================================================
// What's New banner (v2 — с историей)
// ============================================================
const WN_VERSION = "''' + NEW_VERSION + '''";
const WN_KEY = "hsk5_whatsnew_dismissed_" + WN_VERSION;

function wnShowBanner() {
  try { if (localStorage.getItem(WN_KEY) === "1") return; } catch (e) {}
  const host = document.getElementById("whatsnew-host");
  if (!host) return;

  host.innerHTML = `
    <div id="wn-banner" style="
      position:relative;
      margin:14px 0 18px;
      padding:18px 20px 16px;
      border-radius:14px;
      background:linear-gradient(135deg, rgba(102,178,255,0.10), rgba(92,214,142,0.08));
      border:1px solid rgba(102,178,255,0.35);
      box-shadow:0 8px 28px rgba(74,158,255,0.15);
      animation:wnFadeIn .5s ease;
    ">
      <style>
        @keyframes wnFadeIn { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:none; } }
        @keyframes wnPop { 0% { transform:scale(.6); } 60% { transform:scale(1.12); } 100% { transform:scale(1); } }
        #wn-banner ul { margin:8px 0 0; padding-left:22px; }
        #wn-banner li { margin:5px 0; color:#D9E6F2; font-size:13.5px; line-height:1.55; }
        #wn-banner b { color:#7EE0FF; }
        #wn-banner .wn-old { margin-top:14px; padding-top:12px; border-top:1px dashed rgba(102,178,255,0.25); }
        #wn-banner .wn-old summary { cursor:pointer; color:#8B9AAB; font-size:12.5px; list-style:none; }
        #wn-banner .wn-old summary::-webkit-details-marker { display:none; }
        #wn-banner .wn-old summary:before { content:"▸ "; color:#7EE0FF; }
        #wn-banner .wn-old[open] summary:before { content:"▾ "; }
        #wn-banner .wn-old-body { margin-top:10px; padding-left:4px; opacity:.85; }
        #wn-banner .wn-old-body h4 { color:#A6B4C2; font-size:12px; text-transform:uppercase; letter-spacing:.4px; margin:10px 0 4px; font-weight:600; }
        #wn-banner .wn-old-body li { font-size:12.5px; color:#A6B4C2; }
      </style>
      <button id="wn-close" type="button" title="Dismiss" style="
        position:absolute;top:8px;right:10px;
        background:transparent;border:0;color:#6E7A8A;
        font-size:20px;cursor:pointer;line-height:1;padding:4px 8px;
      ">✕</button>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
        <span style="font-size:24px;animation:wnPop .5s ease">🚀</span>
        <span style="font-size:16px;font-weight:700;color:#E6EDF5">What's new — September 28, 2026</span>
      </div>
      <div style="font-size:13px;color:#A6B4C2;margin-bottom:6px">
        Big update: a whole new Business Chinese course and audio for lessons.
      </div>
      <ul>
        <li><b>New: Business Chinese (商务中文)</b> — 5 modules, 15 lessons, full curriculum. Separate dashboard reachable from the top-right button 💼 on the main screen.</li>
        <li><b>Lesson 1 fully developed</b> — 2 dialogs (airport + hotel), 17 vocabulary cards with detailed explanations, 4 expressions, 5 grammar patterns, and exercises (comprehension, true/false, multiple choice, fill-in-the-blank).</li>
        <li><b>Audio for Lesson 1</b> — listen to dialogs and vocabulary with the built-in player: play / ±5s / speed 0.5×–2.0×.</li>
        <li><b>Business content in 6 languages</b> — Russian, English, Türkmen, O'zbek, Тоҷикӣ, Indonesia. Auto-syncs with the language you chose in HSK 5.</li>
        <li><b>Business lessons accessible</b> — click any module or lesson on the Business dashboard to open it. Progress markup and "Start training" buttons work.</li>
        <li><b>Retranslated Turkmen</b> — the entire HSK 5 course and Business now use the fresh DeepSeek translation (better quality).</li>
      </ul>

      <details class="wn-old">
        <summary>Previous updates (Sep 26, 2026)</summary>
        <div class="wn-old-body">
          <h4>Translations & SRS</h4>
          <ul>
            <li><b>6 languages</b> — English, Русский, Türkmen, O'zbek, Тоҷикӣ, Indonesia. Full UI + lesson translations.</li>
            <li><b>Anki-style SRS</b> — learning steps (1m → 10m → 1d), ease factor, lapses, delay bonus. Exactly like AnkiDroid.</li>
            <li><b>SRS settings</b> — tweak learning steps, graduating interval, ease, easy bonus, and more.</li>
            <li><b>SRS stats</b> — retention rate, state distribution, 7-day forecast.</li>
            <li><b>Lesson picker in SRS</b> — pick specific lessons before reviewing.</li>
            <li><b>Audio on SRS cards</b> — tap 🔊 to hear the word (836 words).</li>
            <li><b>Export / Import SRS</b> — JSON backup for moving between devices.</li>
            <li><b>Animated SRS tutorial</b> — tap the "?" button for a quick guide.</li>
            <li><b>Language picker on first launch</b> — choose your language right away.</li>
            <li><b>Feedback form</b> now works in all 6 languages.</li>
            <li><b>Lesson content</b> — all 18 lessons fully translated to uz / tg / id.</li>
            <li><b>Removed</b> the old "Täze täzelikler" banner.</li>
          </ul>
          <h4>Grammar & Content</h4>
          <ul>
            <li><b>Detailed HSK 5 grammar</b> — all 64 points get formula, when-to-use, common mistakes, comparison, and exercises.</li>
            <li><b>Grammar UI</b> — new blocks render on every grammar card.</li>
          </ul>
        </div>
      </details>
    </div>`;

  const x = document.getElementById("wn-close");
  if (x) x.addEventListener("click", function () {
    const b = document.getElementById("wn-banner");
    if (b) { b.style.transition = "opacity .25s"; b.style.opacity = "0"; setTimeout(function(){ b.remove(); }, 250); }
    try { localStorage.setItem(WN_KEY, "1"); } catch (e) {}
  });
}
'''


def main():
    src = APP.read_text(encoding="utf-8")

    # Найдём старую версию
    m_ver = re.search(r'const WN_VERSION = "([^"]+)"', src)
    if m_ver:
        old_ver = m_ver.group(1)
        print(f"Старая версия: {old_ver}")
    else:
        print("!! не нашёл const WN_VERSION — баннер не установлен?")
        return

    # Найдём границы функции wnShowBanner
    m = re.search(r'(//\s*=+\s*\n//\s*What\'s New banner[^\n]*\n//\s*=+\s*\n)?'
                  r'const WN_VERSION = "[^"]+";.*?^}$',
                  src, re.DOTALL | re.MULTILINE)
    if not m:
        print("!! не нашёл блок What's New (const WN_VERSION … wnShowBanner)")
        return

    block_start = m.start()
    block_end = m.end()

    new_src = src[:block_start] + NEW_BANNER_JS.strip() + src[block_end:]

    # Проверка баланса
    if new_src.count("{") != new_src.count("}"):
        print(f"!! {{ }} разбаланс: {new_src.count('{')}/{new_src.count('}')}")
        return
    if new_src.count("`") % 2 != 0:
        print(f"!! backtick нечётный: {new_src.count('`')}")
        return

    bak = APP.with_suffix(APP.suffix + ".pre_banner_v3.bak")
    shutil.copy2(APP, bak)
    APP.write_text(new_src, encoding="utf-8")
    print(f"OK: баннер обновлён → {NEW_VERSION}")
    print(f"Бэкап: {bak.name}")
    print()
    print("Проверка:")
    print("  - новая версия v3 (все увидят заново)")
    print("  - сверху: Business Chinese + audio + 6 языков")
    print("  - снизу раскрывающийся «Previous updates (Sep 26, 2026)»")
    print()
    print("Дальше: Ctrl+Shift+R в браузере (сервер не трогаем)")


if __name__ == "__main__":
    main()