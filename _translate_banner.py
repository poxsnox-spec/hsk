#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Переводит баннер What's New на все 7 языков и патчит app.js."""
import json
import os
import shutil
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
APP = ROOT / "web" / "static" / "app.js"
CACHE = ROOT / "_banner_tr_cache.json"

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY", "") if 32 < ord(c) < 127)
BASE = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

# ---------- Английский источник ----------
EN_CONTENT = {
    "title": "What's new — October 2, 2026",
    "subtitle": "Turkish is here! Now 7 languages across the whole app — UI, HSK 6 words, HSK 5 lessons, and Business Chinese.",
    "items": [
        {"t": "New language: Türkçe (tr)", "d": "The full interface is now available in Turkish: menus, buttons, labels, every screen. Pick it from the globe button 🌐 in the bottom-right corner."},
        {"t": "HSK 6 words in Turkish", "d": "All 2,460 vocabulary entries now have Turkish translations, alongside Russian, English, Turkmen, Uzbek, Tajik, and Indonesian."},
        {"t": "HSK 5 lessons in Turkish", "d": "All 18 lessons fully translated: titles, vocabulary, grammar explanations, comparisons, exercises."},
        {"t": "Business Chinese in Turkish", "d": "All 15 lessons of the business course now fully readable in Turkish."},
        {"t": "Flag icons in the language picker", "d": "The popup now shows clean circular flags for every language, loaded from a fast CDN and rendered identically on Windows, macOS, Linux, iOS and Android."},
        {"t": "HSK 6 TTS reader", "d": "One round 🔊 button in the top-right corner of the HSK 6 card. Click it once: the app reads the whole card in sequence — character → pinyin → translation → deep explanation → every example. Click again to stop. Press R to toggle it from the keyboard."},
        {"t": "Back to the main app", "d": "A small ← HSK 5 Learner button now sits in the top-left corner of every HSK 6 screen, so you can jump back instantly without losing progress."},
        {"t": "Automatic SRS additions", "d": "If you spend more than 1 minute on a word, it's automatically added to your SRS deck. No extra clicks."},
    ],
    "prev": {
        "label": "Previous updates (Oct 1, 2026) — HSK 6 module",
        "items": [
            {"t": "New: HSK 6 module (中文 HSK 6)", "d": "A standalone learning section with the full official HSK 6 vocabulary list: 2,460 words, each with pinyin and translations."},
            {"t": "Deep AI explanations", "d": "For every word — powered by DeepSeek: meaning, when it's used, when it's not used, collocations, nuance vs. synonyms, register."},
            {"t": "3 example sentences per word", "d": "Everyday, journalistic, and abstract/academic registers, with pinyin and translation."},
            {"t": "Yellow highlighting of other HSK6 words", "d": "Inside every example sentence."},
            {"t": "Anki-style SRS for HSK 6", "d": "Separate deck with Again / Hard / Good / Easy, learning steps, ease, lapses."},
            {"t": "Smart SQLite cache", "d": "Each generated explanation is shared across all users; repeat views cost zero API tokens."},
            {"t": "Google Analytics 4 + Search Console", "d": "Set up for traffic insights."},
            {"t": "sitemap.xml + robots.txt", "d": "For proper indexing by Google and other search engines."},
        ],
    },
    "older": {
        "label": "Even earlier (Sep 28, 2026) — Business Chinese",
        "items": [
            {"t": "New: Business Chinese (商务中文)", "d": "5 modules, 15 lessons, full curriculum. Reachable from the top-right 🧳 button on the main screen."},
            {"t": "Lesson 1 fully developed", "d": "2 dialogs (airport + hotel), 17 vocabulary cards with detailed explanations, 4 expressions, 5 grammar patterns, and exercises."},
            {"t": "Audio for Lesson 1", "d": "With the built-in player: play / ±5s / speed 0.5×–2.0×."},
            {"t": "Retranslated Turkmen", "d": "The entire HSK 5 course and Business now use a fresh DeepSeek translation."},
        ],
        "older": {
            "label": "Even earlier (Sep 26, 2026) — Translations & SRS",
            "sections": [
                {"h": "Translations & SRS", "items": [
                    {"t": "6 languages", "d": "English, Русский, Türkmen, O'zbek, Тоҷикӣ, Indonesia. Full UI + lesson translations."},
                    {"t": "Anki-style SRS", "d": "Learning steps (1m → 10m → 1d), ease factor, lapses, delay bonus."},
                    {"t": "SRS settings", "d": "Tweak learning steps, graduating interval, ease, easy bonus, and more."},
                    {"t": "SRS stats", "d": "Retention rate, state distribution, 7-day forecast."},
                    {"t": "Lesson picker in SRS", "d": "Pick specific lessons before reviewing."},
                    {"t": "Audio on SRS cards", "d": "Tap 🔊 to hear the word (836 words)."},
                    {"t": "Export / Import SRS", "d": "JSON backup for moving between devices."},
                ]},
                {"h": "Grammar & Content", "items": [
                    {"t": "Detailed HSK 5 grammar", "d": "All 64 points get formula, when-to-use, common mistakes, comparison, and exercises."},
                ]},
            ],
        },
    },
}

LANG_NAMES = {
    "ru": "Russian",
    "tk": "Turkmen",
    "uz": "Uzbek",
    "tg": "Tajik",
    "id": "Indonesian",
    "tr": "Turkish",
}
ALL_LANGS = ["en", "ru", "tk", "uz", "tg", "id", "tr"]


def translate(content, target_lang_name):
    prompt = (
        f"Translate this JSON from English to {target_lang_name}. "
        f"Keep the exact same structure and keys — translate only the string values. "
        f"Keep HTML tags <b>...</b>, <i>...</i>, emojis (🌐 🔊 ← → 🧳 🇹🇷 ± ×), "
        f"numbers, and product names (HSK, HSK 5, HSK 6, DeepSeek, SQLite, "
        f"Google Analytics, Search Console, sitemap.xml, robots.txt, Anki, CDN, "
        f"Windows, macOS, Linux, iOS, Android, Business Chinese, Türkçe, "
        f"Русский, Türkmen, O'zbek, Тоҷикӣ, Indonesia) as-is. "
        f"Return ONLY valid JSON, no markdown fences.\n\n"
        f"JSON:\n{json.dumps(content, ensure_ascii=False)}"
    )
    for attempt in range(3):
        try:
            r = requests.post(
                BASE,
                headers={"Authorization": "Bearer " + API_KEY,
                         "Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "system",
                         "content": "You are a professional translator. Return only valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
                timeout=180,
            )
            if r.status_code == 200:
                return json.loads(r.json()["choices"][0]["message"]["content"])
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(2)
    raise RuntimeError(f"DeepSeek не отвечает для {target_lang_name}")


# ---------- JS-рендер ----------
JS_TEMPLATE = '''const WN_VERSION = "2026-10-02-turkish-i18n";
const WN_KEY = "hsk5_whatsnew_dismissed_" + WN_VERSION;

const WN_CONTENT = %s;

function wnShowBanner() {
  try { if (localStorage.getItem(WN_KEY) === "1") return; } catch (e) {}
  const host = document.getElementById("whatsnew-host");
  if (!host) return;

  const lang = (typeof getLang === "function") ? getLang() : "en";
  const C = WN_CONTENT[lang] || WN_CONTENT.en;

  const renderItems = (items) => (items || []).map(it =>
    `<li><b>${it.t}</b> — ${it.d}</li>`
  ).join("");

  host.innerHTML = `
    <div id="wn-banner" style="
      position:relative;
      margin:14px 0 18px;
      padding:18px 20px 16px;
      border-radius:14px;
      background:linear-gradient(135deg, rgba(225,29,72,0.10), rgba(240,180,40,0.06));
      border:1px solid rgba(225,29,72,0.35);
      box-shadow:0 8px 28px rgba(225,29,72,0.14);
      animation:wnFadeIn .5s ease;
    ">
      <style>
        @keyframes wnFadeIn { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:none; } }
        @keyframes wnPop { 0% { transform:scale(.6); } 60% { transform:scale(1.12); } 100% { transform:scale(1); } }
        #wn-banner ul { margin:8px 0 0; padding-left:22px; }
        #wn-banner li { margin:5px 0; color:#D9E6F2; font-size:13.5px; line-height:1.55; }
        #wn-banner b { color:#FF9AA6; }
        #wn-banner .wn-old { margin-top:14px; padding-top:12px; border-top:1px dashed rgba(225,29,72,0.25); }
        #wn-banner .wn-old summary { cursor:pointer; color:#8B9AAB; font-size:12.5px; list-style:none; }
        #wn-banner .wn-old summary::-webkit-details-marker { display:none; }
        #wn-banner .wn-old summary:before { content:"▸ "; color:#FF9AA6; }
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
        <span style="font-size:24px;animation:wnPop .5s ease">🇹🇷</span>
        <span style="font-size:16px;font-weight:700;color:#E6EDF5">${C.title}</span>
      </div>
      <div style="font-size:13px;color:#A6B4C2;margin-bottom:6px">${C.subtitle}</div>
      <ul>${renderItems(C.items)}</ul>

      <details class="wn-old">
        <summary>${C.prev.label}</summary>
        <div class="wn-old-body">
          <ul>${renderItems(C.prev.items)}</ul>

          <details class="wn-old" style="margin-top:14px">
            <summary>${C.older.label}</summary>
            <div class="wn-old-body">
              <ul>${renderItems(C.older.items)}</ul>

              <details class="wn-old" style="margin-top:14px">
                <summary>${C.older.older.label}</summary>
                <div class="wn-old-body">
                  ${C.older.older.sections.map(s =>
                    `<h4>${s.h}</h4><ul>${renderItems(s.items)}</ul>`
                  ).join("")}
                </div>
              </details>
            </div>
          </details>
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
    if not API_KEY:
        print("!! set DEEPSEEK_API_KEY=sk-... и повтори")
        sys.exit(1)

    # Кэш переводов
    cache = {}
    if CACHE.exists():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
            print(f"Кэш: {len(cache)} языков")
        except Exception:
            cache = {}

    translations = {"en": EN_CONTENT}
    for lang in ALL_LANGS:
        if lang == "en":
            continue
        if lang in cache:
            print(f"[{lang}] из кэша")
            translations[lang] = cache[lang]
            continue
        print(f"[{lang}] перевод через DeepSeek ({LANG_NAMES[lang]})...")
        try:
            translations[lang] = translate(EN_CONTENT, LANG_NAMES[lang])
            cache[lang] = translations[lang]
            CACHE.write_text(
                json.dumps(cache, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            print(f"  !! ошибка: {e}")
            translations[lang] = EN_CONTENT

    # Генерируем JS
    content_js = json.dumps(translations, ensure_ascii=False, indent=2)
    new_banner_js = JS_TEMPLATE % content_js

    # Патчим app.js
    src = APP.read_text(encoding="utf-8")
    start_marker = "const WN_VERSION = "
    end_marker = "function renderMainMenu()"
    start_idx = src.find(start_marker)
    end_idx = src.find(end_marker, start_idx) if start_idx >= 0 else -1

    if start_idx < 0 or end_idx < 0:
        print("!! не нашёл блок баннера в app.js")
        return

    new_src = src[:start_idx] + new_banner_js + "\n\n" + src[end_idx:]

    bak = APP.with_suffix(APP.suffix + ".pre_banner_i18n.bak")
    shutil.copy2(APP, bak)
    APP.write_text(new_src, encoding="utf-8")

    print(f"\nOK: app.js обновлён. Бэкап: {bak.name}")
    print(f"Кэш: {CACHE.name} ({len(cache)} языков)")
    print("\nПерезапусти сервер и обнови браузер (Ctrl+Shift+R).")


if __name__ == "__main__":
    main()