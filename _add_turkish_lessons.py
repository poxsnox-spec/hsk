#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дополняет JSON уроков (HSK5 + Business) переводом на турецкий (tr).

Алгоритм:
1. Проходим все JSON-файлы, собираем уникальные английские строки.
2. Отправляем их в DeepSeek батчами -> получаем турецкий.
3. Вторым проходом дописываем поле 'tr' во все словари-переводы.

Идемпотентно: повторный запуск не трогает уже переведённые блоки.
"""
import json
import os
import shutil
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DIRS = [
    ROOT / "data" / "lessons",
    ROOT / "data" / "business",
]

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY", "") if 32 < ord(c) < 127)
BASE = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

LANG_KEYS = {"ru", "en", "tk", "uz", "tg", "id"}
SRC = "en"
DST = "tr"
BATCH_SIZE = 40
CACHE_FILE = ROOT / "_tr_cache.json"


# ---------- DeepSeek ----------
def translate_batch(items):
    """items: [{id, text}, ...] -> {id: text_tr}"""
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY не задан")
    prompt = (
        "Translate the following English UI/lesson texts into Turkish. "
        "Keep meaning, tone, punctuation, placeholders ({name}, %), emojis. "
        "Return JSON: {\"items\":[{\"id\":\"<id>\",\"tr\":\"<turkish>\"}]}\n\n"
        f"Texts:\n{json.dumps(items, ensure_ascii=False)}"
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
                         "content": "Return ONLY valid JSON, no markdown."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
                timeout=180,
            )
            if r.status_code == 200:
                data = json.loads(r.json()["choices"][0]["message"]["content"])
                return {
                    it["id"]: it["tr"]
                    for it in data.get("items", [])
                    if "id" in it and "tr" in it
                }
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(2)
    raise RuntimeError("DeepSeek не отвечает")


# ---------- Обход JSON ----------
def is_lang_map(d):
    """Словарь-перевод: имеет английский ключ и другие языковые ключи."""
    if not isinstance(d, dict):
        return False
    ks = set(d.keys())
    return bool(ks & LANG_KEYS) and len(ks) <= 10 and SRC in d


def walk(node, fn):
    if isinstance(node, dict):
        fn(node)
        for v in node.values():
            walk(v, fn)
    elif isinstance(node, list):
        for v in node:
            walk(v, fn)


def collect_texts(node, texts):
    if isinstance(node, str):
        if node.strip():
            texts.add(node)
    elif isinstance(node, list):
        for x in node:
            if isinstance(x, str) and x.strip():
                texts.add(x)


def collect_from_file(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    texts = set()

    def visit(n):
        if is_lang_map(n) and DST not in n:
            collect_texts(n.get(SRC), texts)

    walk(data, visit)
    return texts


def apply_translations(node, cache):
    if isinstance(node, dict):
        if is_lang_map(node) and DST not in node:
            src_val = node.get(SRC)
            if isinstance(src_val, str):
                tr = cache.get(src_val)
                if tr:
                    node[DST] = tr
            elif isinstance(src_val, list):
                node[DST] = [
                    cache.get(x, x) if isinstance(x, str) else x
                    for x in src_val
                ]
        for v in node.values():
            apply_translations(v, cache)
    elif isinstance(node, list):
        for v in node:
            apply_translations(v, cache)


def iter_files():
    for base in DIRS:
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.json")):
            if p.name.startswith("."):
                continue
            if p.suffix == ".bak":
                continue
            yield p


# ---------- Main ----------
def main():
    if not API_KEY:
        print("!! Установи DEEPSEEK_API_KEY в этом окне: set DEEPSEEK_API_KEY=sk-...")
        sys.exit(1)

    files = list(iter_files())
    if not files:
        print("!! Не нашёл JSON в data/lessons или data/business")
        sys.exit(1)
    print(f"Найдено {len(files)} JSON-файлов")

    # 1) Собираем тексты
    print("\n[1/3] Собираю английские тексты для перевода…")
    all_texts = set()
    for f in files:
        try:
            all_texts |= collect_from_file(f)
        except Exception as e:
            print(f"   skip {f.name}: {e}")
    print(f"Уникальных строк: {len(all_texts)}")

    # 2) Грузим кэш
    cache = {}
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            print(f"Кэш: {len(cache)} строк")
        except Exception:
            cache = {}

    todo = [t for t in sorted(all_texts) if t not in cache]
    print(f"К переводу: {len(todo)}")

    if todo:
        print("\n[2/3] Перевод через DeepSeek…")
        total_batches = (len(todo) + BATCH_SIZE - 1) // BATCH_SIZE
        for bi, i in enumerate(range(0, len(todo), BATCH_SIZE), 1):
            chunk = todo[i:i + BATCH_SIZE]
            items = [{"id": f"s{idx}", "text": t} for idx, t in enumerate(chunk)]
            print(f"   [{bi}/{total_batches}] строк {i+1}-{i+len(chunk)}")
            try:
                result = translate_batch(items)
                for idx, t in enumerate(chunk):
                    sid = f"s{idx}"
                    if sid in result:
                        cache[t] = result[sid]
            except Exception as e:
                print(f"   !! fail: {e}")
            # сохраняем кэш после каждого батча
            CACHE_FILE.write_text(
                json.dumps(cache, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
    else:
        print("\nНечего переводить — всё в кэше")

    # 3) Применяем
    print("\n[3/3] Применяю переводы к файлам…")
    changed = 0
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"   skip {f.name}: {e}")
            continue
        bak = f.with_suffix(f.suffix + ".pre_tr.bak")
        if not bak.exists():
            shutil.copy2(f, bak)
        apply_translations(data, cache)
        f.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        changed += 1
        print(f"   ok: {f.relative_to(ROOT)}")

    print(f"\nГОТОВО. Обновлено файлов: {changed}")
    print(f"Кэш: {CACHE_FILE.name} ({len(cache)} строк)")
    print("\nДальше:")
    print("  1) Проверь локально (перезапусти сервер + Ctrl+Shift+R)")
    print("  2) git add data/ web/static/i18n.js web/static/hsk6.js web/hsk6.py")
    print("  3) git commit -m \"feat(i18n): Turkish (tr) for HSK5 + Business lessons\"")
    print("  4) git push; на PythonAnywhere: git pull + Reload")


if __name__ == "__main__":
    main()