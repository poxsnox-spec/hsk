#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет новый пункт про i18n баннера в WN_CONTENT и переводит на 6 языков."""
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

# Новый пункт на английском — вставляем в начало списка
NEW_ITEM_EN = {
    "t": "The banner now follows your language",
    "d": "This What's New banner is now fully translated — switch the interface language and it changes with you, just like the rest of the app.",
}

LANG_NAMES = {
    "ru": "Russian",
    "tk": "Turkmen",
    "uz": "Uzbek",
    "tg": "Tajik",
    "id": "Indonesian",
    "tr": "Turkish",
}


def translate_item(target_lang_name):
    prompt = (
        f"Translate the following JSON from English to {target_lang_name}. "
        f"Keep the exact same structure and keys — translate only the string values. "
        f"Keep emojis, numbers, product names (HSK, DeepSeek, What's New) as-is. "
        f"Return ONLY valid JSON, no markdown fences.\n\n"
        f"JSON:\n{json.dumps(NEW_ITEM_EN, ensure_ascii=False)}"
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
                timeout=60,
            )
            if r.status_code == 200:
                return json.loads(r.json()["choices"][0]["message"]["content"])
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(2)
    raise RuntimeError(f"DeepSeek не отвечает для {target_lang_name}")


def main():
    if not API_KEY:
        print("!! set DEEPSEEK_API_KEY=sk-... и повтори")
        sys.exit(1)
    if not CACHE.exists():
        print(f"!! нет кэша {CACHE.name}")
        return

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    print(f"Кэш: {list(cache.keys())}")

    # Переводим новый пункт
    new_items = {"en": NEW_ITEM_EN}
    for lang, lname in LANG_NAMES.items():
        print(f"[{lang}] перевод пункта ({lname})...")
        try:
            new_items[lang] = translate_item(lname)
        except Exception as e:
            print(f"  !! {e}")
            new_items[lang] = NEW_ITEM_EN

    # Вставляем пункт в начало items для каждого языка
    for lang in ["en", "ru", "tk", "uz", "tg", "id", "tr"]:
        if lang in cache:
            cache[lang].setdefault("items", [])
            # если этот пункт уже есть — пропускаем
            first = cache[lang]["items"][0] if cache[lang]["items"] else {}
            if "What's New" in (first.get("d") or "") or "баннер" in (first.get("d") or "").lower():
                print(f"  {lang}: уже есть в начале — пропускаю")
                continue
            cache[lang]["items"].insert(0, new_items[lang])
        elif lang == "en":
            # EN обновим в fix-скрипте — тут просто сохраним
            pass

    # EN добавим тоже в кэш (хотя fix использует свой хардкод)
    if "en" not in cache:
        cache["en"] = {"items": [NEW_ITEM_EN]}
    else:
        if not (cache["en"].get("items") and "What's New" in cache["en"]["items"][0].get("d", "")):
            cache["en"].setdefault("items", []).insert(0, NEW_ITEM_EN)

    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOK: пункт добавлен в кэш для 7 языков. {CACHE.name} обновлён.")
    print("Дальше: запусти _translate_banner_fix.py — пересоберёт баннер в app.js")


if __name__ == "__main__":
    main()