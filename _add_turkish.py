#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет турецкий (tr) в i18n.js, hsk6.js и web/hsk6.py через DeepSeek."""
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
I18N = ROOT / "web" / "static" / "i18n.js"
HSK6 = ROOT / "web" / "static" / "hsk6.js"
HSK6_PY = ROOT / "web" / "hsk6.py"

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY", "") if 32 < ord(c) < 127)
BASE = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

LANG_NAME = "Türkçe (Turkish)"


def call_deepseek(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY не задан в env")
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
                         "content": "You are a professional translator. Return ONLY valid JSON, no explanations, no markdown fences."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
                timeout=180,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"   retry {attempt+1}: {e}")
        time.sleep(2)
    raise RuntimeError("DeepSeek не отвечает")


# ============================================================
# ПАРСИНГ JS-ОБЪЕКТОВ
# ============================================================
def extract_js_object(src: str, key: str) -> str | None:
    """Возвращает текст { ... } для ключа key внутри STRINGS/T6, включая фигурные скобки."""
    # ищем `key: {` в контексте
    pattern = re.compile(rf'(\b{re.escape(key)}\s*:\s*\{{)')
    m = pattern.search(src)
    if not m:
        return None
    # с этой позиции идём вперёд, считая скобки
    start = m.end() - 1  # позиция первой {
    depth = 0
    i = start
    in_str = False
    str_ch = ""
    escaped = False
    while i < len(src):
        ch = src[i]
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == str_ch:
                in_str = False
        else:
            if ch in ("'", '"', "`"):
                in_str = True
                str_ch = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return src[start:i+1]
        i += 1
    return None


def parse_flat_js_object(obj_text: str) -> dict:
    """Парсит плоский JS-объект с парами 'key': 'value' (без вложенности, только строки)."""
    # удаляем внешние {}
    inner = obj_text.strip()[1:-1]
    result = {}
    # паттерн: "key": "value" или 'key': 'value' или key: "value"
    pattern = re.compile(
        r'(?P<key>"[^"]+"|\'[^\']+\'|[A-Za-z_][A-Za-z0-9_]*)'
        r'\s*:\s*'
        r'(?P<val>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')',
        re.DOTALL,
    )
    for m in pattern.finditer(inner):
        k = m.group("key").strip("\"'")
        v = m.group("val")[1:-1]
        # разэкранируем \\" и \\'
        v = v.replace('\\"', '"').replace("\\'", "'").replace("\\\\", "\\")
        result[k] = v
    return result


def js_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def render_js_object(pairs: dict) -> str:
    """Собирает JS-объект { ... } с 4-пробельным отступом."""
    lines = []
    for k, v in pairs.items():
        lines.append(f'    {k}: "{js_escape(v)}",')
    return "{\n" + "\n".join(lines) + "\n  }"


# ============================================================
# ПЕРЕВОД
# ============================================================
def translate_batch(pairs: dict, context: str) -> dict:
    """Отправляет пары { key: english_value } → возвращает { key: turkish_value }."""
    items = [{"key": k, "text": v} for k, v in pairs.items()]
    prompt = (
        f"Translate the following UI strings from English to {LANG_NAME}.\n"
        f"Context: {context}\n"
        f"Return JSON with the same 'key's and translated 'text' values "
        f"(value shape: {{\"items\": [{{\"key\":\"...\",\"text\":\"...\"}}, ...]}}).\n"
        f"Keep placeholders like {{name}}, %, emojis, and markup as-is.\n\n"
        f"Strings:\n{json.dumps(items, ensure_ascii=False)}"
    )
    resp = call_deepseek(prompt)
    data = json.loads(resp)
    out = {}
    for item in data.get("items", []):
        k = item.get("key")
        t = item.get("text")
        if k and t is not None:
            out[k] = str(t)
    return out


def translate_in_chunks(pairs: dict, context: str, chunk_size: int = 60) -> dict:
    keys = list(pairs.keys())
    result = {}
    for i in range(0, len(keys), chunk_size):
        chunk_keys = keys[i:i + chunk_size]
        chunk = {k: pairs[k] for k in chunk_keys}
        print(f"   перевод {i+1}-{i+len(chunk_keys)} из {len(keys)}")
        try:
            translated = translate_batch(chunk, context)
        except Exception as e:
            print(f"   !! ошибка батча: {e}")
            translated = {}
        for k in chunk_keys:
            result[k] = translated.get(k, pairs[k])  # fallback — англ.
    return result


# ============================================================
# ПАТЧ i18n.js
# ============================================================
def patch_i18n():
    src = I18N.read_text(encoding="utf-8")
    if re.search(r'\btr\s*:\s*\{', src):
        print("i18n.js: tr уже есть")
        return
    en_block = extract_js_object(src, "en")
    if not en_block:
        print("i18n.js: не нашёл блок en")
        return
    en_pairs = parse_flat_js_object(en_block)
    print(f"i18n.js: en содержит {len(en_pairs)} ключей")
    tr_pairs = translate_in_chunks(en_pairs, "HSK Chinese learning app UI")

    # собираем блок tr и вставляем после блока ru или в конце STRINGS
    tr_block = f"  tr: {render_js_object(tr_pairs)},\n"

    # ищем `const STRINGS = {` и вставляем сразу после него
    m = re.search(r'(const\s+STRINGS\s*=\s*\{)', src)
    if not m:
        print("i18n.js: не нашёл const STRINGS")
        return
    insert_pos = m.end()
    new_src = src[:insert_pos] + "\n" + tr_block + src[insert_pos:]

    bak = I18N.with_suffix(I18N.suffix + ".pre_tr.bak")
    shutil.copy2(I18N, bak)
    I18N.write_text(new_src, encoding="utf-8")
    print(f"i18n.js: OK, добавлено {len(tr_pairs)} ключей. Бэкап: {bak.name}")


# ============================================================
# ПАТЧ hsk6.js (T6)
# ============================================================
def patch_hsk6():
    src = HSK6.read_text(encoding="utf-8")
    if re.search(r'\btr\s*:\s*\{', src):
        print("hsk6.js: tr уже есть")
        return
    en_block = extract_js_object(src, "en")
    if not en_block:
        print("hsk6.js: не нашёл блок en")
        return
    en_pairs = parse_flat_js_object(en_block)
    print(f"hsk6.js: T6.en содержит {len(en_pairs)} ключей")
    tr_pairs = translate_in_chunks(en_pairs, "HSK6 UI: buttons, labels, SRS")

    tr_block = f"  tr: {render_js_object(tr_pairs)},\n"

    m = re.search(r'(const\s+T6\s*=\s*\{)', src)
    if not m:
        print("hsk6.js: не нашёл const T6")
        return
    insert_pos = m.end()
    new_src = src[:insert_pos] + "\n" + tr_block + src[insert_pos:]

    # добавляем tr в LANG_MAP (для TTS)
    new_src = re.sub(
        r'(id:\s*\["id-ID",\s*"id",\s*"en-US"\],)',
        r'\1\n    tr: ["tr-TR", "tr", "en-US"],',
        new_src,
        count=1,
    )

    bak = HSK6.with_suffix(HSK6.suffix + ".pre_tr.bak")
    shutil.copy2(HSK6, bak)
    HSK6.write_text(new_src, encoding="utf-8")
    print(f"hsk6.js: OK. Бэкап: {bak.name}")


# ============================================================
# ПАТЧ web/hsk6.py
# ============================================================
def patch_hsk6_py():
    src = HSK6_PY.read_text(encoding="utf-8")
    if '"tr"' in src:
        print("web/hsk6.py: tr уже есть")
        return
    src = src.replace(
        'LANGS = ["ru", "en", "tk", "uz", "tg", "id"]',
        'LANGS = ["ru", "en", "tk", "uz", "tg", "id", "tr"]',
    )
    src = src.replace(
        '"uz": "o\'zbek tili", "tg": "тоҷикӣ", "id": "Bahasa Indonesia",',
        '"uz": "o\'zbek tili", "tg": "тоҷикӣ", "id": "Bahasa Indonesia",\n    "tr": "Türkçe",',
    )
    bak = HSK6_PY.with_suffix(HSK6_PY.suffix + ".pre_tr.bak")
    shutil.copy2(HSK6_PY, bak)
    HSK6_PY.write_text(src, encoding="utf-8")
    print(f"web/hsk6.py: OK. Бэкап: {bak.name}")


def main():
    if not API_KEY:
        print("!! Установи DEEPSEEK_API_KEY в этом окне: set DEEPSEEK_API_KEY=sk-...")
        sys.exit(1)
    print("=" * 60)
    print("ДОБАВЛЕНИЕ ТУРЕЦКОГО ЯЗЫКА")
    print("=" * 60)
    patch_i18n()
    print()
    patch_hsk6()
    print()
    patch_hsk6_py()
    print()
    print("=" * 60)
    print("ГОТОВО. Дальше:")
    print("  git add web/static/i18n.js web/static/hsk6.js web/hsk6.py")
    print('  git commit -m "feat(i18n): add Turkish (tr) as 7th language"')
    print("  git push")


if __name__ == "__main__":
    main()