# -*- coding: utf-8 -*-
"""Перевод HSK5 (下册, unit7-12) на tk/uz/tg/id/tr через DeepSeek.

Использует requests напрямую (без openai SDK).
Перезапускаемо — кэш уже переведённого лежит в _translate_cache.json.
"""
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "data" / "lessons"
CACHE_FILE = ROOT / "_translate_cache.json"
KEY_FILE = ROOT / ".deepseek_key"

TARGET_LANGS = ["tk", "uz", "tg", "id", "tr"]

LANG_NAMES = {
    "tk": "Turkmen (Türkmençe)",
    "uz": "Uzbek (O'zbekcha)",
    "tg": "Tajik (Тоҷикӣ)",
    "id": "Indonesian (Bahasa Indonesia)",
    "tr": "Turkish (Türkçe)",
}

API_URL = "https://api.deepseek.com/v1/chat/completions"
TIMEOUT = 90

SYSTEM_PROMPT = """You are a professional translator for a Chinese language learning app (HSK 5).

You will receive Chinese source text and existing Russian/English translations.
Task: translate the source text into the requested target languages.

Rules:
1. Translate ACCURATELY, preserving educational meaning.
2. Keep Chinese characters in the translation when they appear in the source.
3. Preserve formatting: line breaks (\\n), punctuation style.
4. Return STRICT JSON: {"<lang_code>": "<translation>", ...}
5. No markdown, no backticks, no commentary — only JSON.
6. If the source is very short (1-2 words), just translate it directly.
"""


def load_key():
    if not KEY_FILE.exists():
        print(f"[!] Нет файла с ключом: {KEY_FILE}")
        sys.exit(1)
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key.startswith("sk-"):
        print(f"[!] Подозрительный ключ: {key[:10]}...")
        sys.exit(1)
    return key


def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache):
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


CACHE = None


def translate(session, source, ru, en):
    global CACHE
    cache_key = f"{source[:200]}|{ru[:100]}|{en[:100]}"
    if cache_key in CACHE and all(l in CACHE[cache_key] for l in TARGET_LANGS):
        return CACHE[cache_key]

    user_msg = (
        f"Source (Chinese):\n{source}\n\n"
        f"Russian (existing):\n{ru}\n\n"
        f"English (existing):\n{en}\n\n"
        f"Translate the SOURCE into: {', '.join(TARGET_LANGS)}.\n"
        f"Return strict JSON: "
        + json.dumps({l: f"<{LANG_NAMES[l]}>" for l in TARGET_LANGS}, ensure_ascii=False)
    )

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {load_key()}",
        "Content-Type": "application/json",
    }

    for attempt in range(3):
        try:
            r = session.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
            if r.status_code != 200:
                print(f"  [!] HTTP {r.status_code}: {r.text[:200]}")
                time.sleep(2)
                continue
            body = r.json()
            raw = body["choices"][0]["message"]["content"]
            data = json.loads(raw)
            result = {l: (data.get(l) or "").strip() for l in TARGET_LANGS}
            CACHE[cache_key] = result
            save_cache(CACHE)
            return result
        except requests.exceptions.Timeout:
            print(f"  [!] Таймаут (попытка {attempt + 1}/3)")
            time.sleep(3)
        except Exception as e:
            print(f"  [!] Ошибка: {e}")
            time.sleep(2)

    return {l: "" for l in TARGET_LANGS}


def fill_lang_dict(obj, source_zh, session):
    if not isinstance(obj, dict):
        return
    ru = obj.get("ru") or ""
    en = obj.get("en") or ""
    missing = [l for l in TARGET_LANGS if not obj.get(l)]
    if not missing:
        return
    if not source_zh and not ru and not en:
        return
    tr = translate(session, source_zh or ru or en, ru, en)
    for l in missing:
        if tr.get(l):
            obj[l] = tr[l]


def process_lesson(path, session):
    data = json.loads(path.read_text(encoding="utf-8"))
    rel = path.relative_to(ROOT)
    print(f"\n>>> {rel}", flush=True)

    t = data.get("title") or {}
    fill_lang_dict(t, t.get("zh", ""), session)

    wq = (data.get("warmup") or {}).get("question") or {}
    fill_lang_dict(wq, "", session)

    tt = data.get("text_translation") or {}
    print(f"    перевод текста...", flush=True)
    fill_lang_dict(tt, data.get("text_zh", "")[:500], session)

    print(f"    словарь ({len(data.get('vocabulary', []))} слов)...", flush=True)
    for v in data.get("vocabulary", []) or []:
        m = v.get("meaning") or {}
        fill_lang_dict(m, v.get("hanzi", ""), session)

    print(f"    грамматика...", flush=True)
    for g in data.get("grammar", []) or []:
        fill_lang_dict(g.get("explanation") or {}, g.get("word", ""), session)
        fill_lang_dict(g.get("formula") or {}, g.get("word", ""), session)
        for ex in g.get("examples", []) or []:
            fill_lang_dict(ex, ex.get("zh", ""), session)

    for c in data.get("comparisons", []) or []:
        fill_lang_dict(c.get("common") or {},
                       c.get("word_a", "") + " vs " + c.get("word_b", ""),
                       session)
        for d in c.get("differences", []) or []:
            if isinstance(d, dict):
                fill_lang_dict(d, "", session)

    exp = data.get("expansion") or {}
    fill_lang_dict(exp.get("topic") or {}, "", session)
    for w in exp.get("words", []) or []:
        fill_lang_dict(w.get("meaning") or {}, w.get("hanzi", ""), session)

    app = data.get("application") or {}
    fill_lang_dict(app.get("discussion") or {}, "", session)
    fill_lang_dict(app.get("writing_prompt") or {}, "", session)

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("    [+] сохранён", flush=True)


def main():
    global CACHE
    CACHE = load_cache()
    print(f"[+] Кэш: {len(CACHE)} записей")

    session = requests.Session()
    session.headers.update({"User-Agent": "HSK5-Learner/1.0"})

    files = []
    for unit_dir in sorted(LESSONS.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit"):
            continue
        try:
            num = int(unit_dir.name.replace("unit", ""))
        except ValueError:
            continue
        if num < 7:
            continue
        files.extend(sorted(unit_dir.glob("lesson*.json")))

    print(f"[+] Уроков: {len(files)}\n")

    for i, f in enumerate(files, 1):
        print(f"=== [{i}/{len(files)}] ===")
        try:
            process_lesson(f, session)
        except KeyboardInterrupt:
            print("\n[!] Прервано пользователем. Кэш сохранён.")
            break
        except Exception as e:
            print(f"    [!] Пропускаю: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()