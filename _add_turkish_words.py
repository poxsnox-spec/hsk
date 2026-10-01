#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дополняет word_meta.translations ключом 'tr' через DeepSeek."""
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DB = ROOT / "hsk6_data" / "hsk6.sqlite"

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY", "") if 32 < ord(c) < 127)
BASE = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
BATCH = 50


def call_deepseek(prompt: str) -> dict:
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY не задан")
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
                         "content": "Return ONLY valid JSON. No explanations, no markdown."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
                timeout=120,
            )
            if r.status_code == 200:
                return json.loads(r.json()["choices"][0]["message"]["content"])
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(2)
    raise RuntimeError("DeepSeek не отвечает")


def main():
    if not API_KEY:
        print("!! set DEEPSEEK_API_KEY=sk-... и повтори")
        sys.exit(1)
    if not DB.exists():
        print(f"!! нет файла {DB}")
        sys.exit(1)

    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    rows = db.execute(
        "SELECT word_id, hanzi, translations FROM word_meta ORDER BY word_id"
    ).fetchall()
    print(f"Всего слов: {len(rows)}")

    # Отбираем те, где tr ещё нет
    todo = []
    for r in rows:
        tr_map = json.loads(r["translations"] or "{}")
        if "tr" not in tr_map or not tr_map["tr"]:
            todo.append({
                "id": r["word_id"],
                "hanzi": r["hanzi"],
                "en": tr_map.get("en", ""),
            })
    print(f"Без турецкого: {len(todo)}")

    total_batches = (len(todo) + BATCH - 1) // BATCH
    for bi, i in enumerate(range(0, len(todo), BATCH), 1):
        chunk = todo[i:i + BATCH]
        print(f"[{bi}/{total_batches}] words {i+1}-{i+len(chunk)}")
        prompt = (
            "Translate each Chinese word into Turkish. Use the English gloss "
            "as a hint. Return JSON: "
            '{"items":[{"id":<id>,"tr":"<turkish translation>"}]}\n\n'
            f"Words:\n{json.dumps(chunk, ensure_ascii=False)}"
        )
        try:
            data = call_deepseek(prompt)
        except Exception as e:
            print(f"   !! fail: {e}")
            continue

        for item in data.get("items", []):
            wid = item.get("id")
            tr_val = item.get("tr", "")
            if not wid or not tr_val:
                continue
            row = db.execute(
                "SELECT translations FROM word_meta WHERE word_id=?", (wid,)
            ).fetchone()
            if not row:
                continue
            tr_map = json.loads(row["translations"] or "{}")
            tr_map["tr"] = tr_val
            db.execute(
                "UPDATE word_meta SET translations=? WHERE word_id=?",
                (json.dumps(tr_map, ensure_ascii=False), wid),
            )
        db.commit()

    # Проверка
    n = db.execute(
        "SELECT COUNT(*) FROM word_meta WHERE translations LIKE '%\"tr\"%'"
    ).fetchone()[0]
    print(f"\nГОТОВО. С турецким: {n}/{len(rows)}")
    db.close()


if __name__ == "__main__":
    main()