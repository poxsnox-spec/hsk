#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет блок «Coming soon» в баннер What's New и пересобирает app.js."""
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

# ---------- Ярлык «Coming soon» — короткий, хардкодим точно ----------
COMING_LABEL = {
    "en": "Coming soon",
    "ru": "Скоро",
    "tk": "Tiz wagtda",
    "uz": "Tez orada",
    "tg": "Ба наздикӣ",
    "id": "Segera hadir",
    "tr": "Çok yakında",
}

# ---------- Английский источник нового блока ----------
COMING_EN_ITEMS = [
    {
        "t": "HSK 5 Workbook exercises",
        "d": "Listening, Reading, and Writing sections on every HSK 5 lesson — real interactive exercises instead of a placeholder.",
    },
    {
        "t": "HSK 5 (Lower) — 下册",
        "d": "The second half of the HSK 5 course: 18 more lessons, doubling the whole curriculum.",
    },
]

LANG_NAMES = {
    "ru": "Russian",
    "tk": "Turkmen",
    "uz": "Uzbek",
    "tg": "Tajik",
    "id": "Indonesian",
    "tr": "Turkish",
}


def translate_items(target_lang_name):
    prompt = (
        f"Translate this JSON array from English to {target_lang_name}. "
        f"Keep the exact structure and keys ('t' and 'd'). Translate only the values. "
        f"Keep product names (HSK 5, HSK 5 Workbook, 下册) and emojis as-is. "
        f"Return ONLY valid JSON, no markdown fences, root must be an object "
        f'like {{"items": [...]}} with the same array.\n\n'
        f"JSON:\n{json.dumps(COMING_EN_ITEMS, ensure_ascii=False)}"
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
                timeout=90,
            )
            if r.status_code == 200:
                data = json.loads(r.json()["choices"][0]["message"]["content"])
                items = data.get("items") or data.get("array") or []
                if len(items) == len(COMING_EN_ITEMS):
                    return items
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(2)
    return COMING_EN_ITEMS


# ---------- JS-шаблон баннера (с блоком Coming soon) ----------
JS_TEMPLATE = r'''const WN_VERSION = "2026-10-02-turkish-i18n-coming";
const WN_KEY = "hsk5_whatsnew_dismissed_" + WN_VERSION;

const WN_CONTENT = __CONTENT__;

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
        #wn-banner .wn-coming {
          margin-top:16px;
          padding:14px 16px 12px;
          border-radius:10px;
          background:linear-gradient(135deg, rgba(240,180,40,0.10), rgba(240,180,40,0.03));
          border:1px solid rgba(240,180,40,0.4);
        }
        #wn-banner .wn-coming-title {
          display:flex; align-items:center; gap:8px;
          font-size:12px; font-weight:700; letter-spacing:.6px;
          text-transform:uppercase; color:#F0C674; margin-bottom:6px;
        }
        #wn-banner .wn-coming ul { margin-top:4px; }
        #wn-banner .wn-coming li { color:#E6D9A6; }
        #wn-banner .wn-coming b { color:#F0C674; }
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

      ${C.coming ? `
      <div class="wn-coming">
        <div class="wn-coming-title">🚧 ${C.coming.label}</div>
        <ul>${renderItems(C.coming.items)}</ul>
      </div>` : ""}

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
    if not CACHE.exists():
        print(f"!! нет кэша {CACHE.name}")
        sys.exit(1)

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    print(f"Кэш до: {list(cache.keys())}")

    # Для каждого языка добавим coming (переводим, если ещё нет)
    for lang in ["ru", "tk", "uz", "tg", "id", "tr", "en"]:
        if lang not in cache:
            continue
        entry = cache[lang]
        if "coming" in entry and entry["coming"].get("items"):
            print(f"  [{lang}] coming уже есть — пропускаю")
            continue

        label = COMING_LABEL.get(lang, COMING_LABEL["en"])
        if lang == "en":
            items = COMING_EN_ITEMS
        else:
            if not API_KEY:
                print(f"  !! нет DEEPSEEK_API_KEY — использую EN для {lang}")
                items = COMING_EN_ITEMS
            else:
                print(f"  [{lang}] перевод coming через DeepSeek…")
                items = translate_items(LANG_NAMES.get(lang, "English"))
        entry["coming"] = {"label": label, "items": items}
        print(f"  [{lang}] coming добавлен")

    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    # Собираем JS
    content_js = json.dumps(cache, ensure_ascii=False, indent=2)
    new_banner_js = JS_TEMPLATE.replace("__CONTENT__", content_js)

    src = APP.read_text(encoding="utf-8")
    start_marker = "const WN_VERSION = "
    end_marker = "function renderMainMenu()"
    start_idx = src.find(start_marker)
    end_idx = src.find(end_marker, start_idx) if start_idx >= 0 else -1

    if start_idx < 0 or end_idx < 0:
        print("!! не нашёл блок баннера в app.js")
        return

    new_src = src[:start_idx] + new_banner_js + "\n\n" + src[end_idx:]

    bak = APP.with_suffix(APP.suffix + ".pre_banner_coming.bak")
    shutil.copy2(APP, bak)
    APP.write_text(new_src, encoding="utf-8")

    print(f"\nOK: app.js пересобран. Бэкап: {bak.name}")
    print("Перезапусти сервер и обнови браузер (Ctrl+Shift+R).")


if __name__ == "__main__":
    main()