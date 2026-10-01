#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DeepSeek: чистит пиньинь + переводит на 6 языков. Батчами по 40 слов."""
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
WORDS = ROOT / "hsk6_data" / "words.json"
DB = ROOT / "hsk6_data" / "hsk6.sqlite"

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY", "") if 32 < ord(c) < 127)
BASE = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

LANGS = ["ru", "en", "tk", "uz", "tg", "id"]
BATCH = 40

SCHEMA = """
CREATE TABLE IF NOT EXISTS word_meta (
    word_id INTEGER PRIMARY KEY,
    hanzi   TEXT NOT NULL,
    pinyin  TEXT,
    translations TEXT,
    order_index INTEGER
);
CREATE TABLE IF NOT EXISTS word_content (
    word_id INTEGER,
    lang TEXT,
    sentences TEXT,
    explanation TEXT,
    model TEXT,
    created_at INTEGER,
    PRIMARY KEY (word_id, lang)
);
"""


def ensure_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB)
    db.executescript(SCHEMA)
    db.commit()
    return db


def seed(db, words):
    for i, w in enumerate(words):
        db.execute(
            "INSERT OR IGNORE INTO word_meta(word_id, hanzi, order_index) VALUES(?,?,?)",
            (w["id"], w["hanzi"], i),
        )
    db.commit()


def chat_json(payload_messages, temperature=0.1):
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY не задан")
    body = {
        "model": MODEL,
        "messages": payload_messages,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    for attempt in range(3):
        try:
            r = requests.post(
                BASE,
                headers={
                    "Authorization": "Bearer " + API_KEY,
                    "Content-Type": "application/json",
                },
                json=body,
                timeout=120,
            )
            if r.status_code == 200:
                return json.loads(r.json()["choices"][0]["message"]["content"])
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("DeepSeek fail после 3 попыток")


def enrich_batch(batch):
    sys_prompt = (
        "Ты — методист китайского HSK6. Тебе дают слова с ГРЯЗНЫМ OCR-пиньинем "
        "и сырым англ. переводом. Верни СТРОГО JSON."
    )
    user_prompt = f"""Исправь пиньинь (тоны знаками, слоги через пробел) и переведи
каждое слово на 6 языков: ru, en, tk, uz, tg, id.

Список:
{json.dumps(batch, ensure_ascii=False)}

Верни JSON:
{{
  "words": [
    {{"id": <номер>,
      "pinyin": "bāo bì",
      "translations": {{"ru":"...","en":"...","tk":"...","uz":"...","tg":"...","id":"..."}}}}
  ]
}}"""
    return chat_json(
        [{"role": "system", "content": sys_prompt},
         {"role": "user", "content": user_prompt}],
        temperature=0.1,
    ).get("words", [])


def main():
    if not API_KEY:
        print("!! DEEPSEEK_API_KEY не задан в env")
        sys.exit(1)
    words = json.loads(WORDS.read_text(encoding="utf-8"))
    print(f"Загружено {len(words)} слов")
    db = ensure_db()
    seed(db, words)

    total_batches = (len(words) + BATCH - 1) // BATCH
    for bi, i in enumerate(range(0, len(words), BATCH), 1):
        chunk = words[i:i + BATCH]
        payload = [{"id": w["id"], "hanzi": w["hanzi"],
                    "pinyin_raw": w["pinyin_raw"],
                    "english_raw": w["english_raw"]} for w in chunk]
        print(f"[{bi}/{total_batches}] words {i+1}-{i+len(chunk)}...")
        try:
            fixed = enrich_batch(payload)
        except Exception as e:
            print(f"   !! fail: {e}")
            continue
        for f in fixed:
            db.execute(
                "UPDATE word_meta SET pinyin=?, translations=? WHERE word_id=?",
                (f.get("pinyin", ""),
                 json.dumps(f.get("translations", {}), ensure_ascii=False),
                 f["id"]),
            )
        db.commit()

    print("ГОТОВО.")


if __name__ == "__main__":
    main()