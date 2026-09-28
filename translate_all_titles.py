#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Переводит title и module_title всех 15 уроков на tk/uz/tg/id."""
import json, os, sys, time, shutil
from pathlib import Path
import requests

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY","") if 32 < ord(c) < 127)
if not API_KEY:
    print("!! нет DEEPSEEK_API_KEY"); sys.exit(1)

BASE = "https://api.deepseek.com/chat/completions"
BIZ = Path("data/business")
LANGS = {
    "tk": "Turkmen (Türkmen dili, Latin script)",
    "uz": "Uzbek (Latin script)",
    "tg": "Tajik (Cyrillic script)",
    "id": "Indonesian (Bahasa Indonesia)",
}


def api(items, lang):
    name = LANGS[lang]
    lines = [
        f"Translate each string into {name}. Source may be English or Russian.",
        "Return JSON array of translations in SAME order.",
        "Keep business/formal tone appropriate for a Chinese business textbook.",
        "", "Input:",
        json.dumps(items, ensure_ascii=False),
        "", "Output (JSON array):",
    ]
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Translate. Output JSON array only."},
            {"role": "user", "content": "\n".join(lines)},
        ],
        "temperature": 0.2, "max_tokens": 4096,
    }, ensure_ascii=False).encode("utf-8")
    r = requests.post(BASE,
        headers={"Authorization": "Bearer " + API_KEY,
                 "Content-Type": "application/json; charset=utf-8"},
        data=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
    txt = r.json()["choices"][0]["message"]["content"].strip()
    if txt.startswith("```"):
        txt = txt.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(txt)


def main():
    # 1. Собираем все title.ru и module_title.ru
    files = sorted(BIZ.glob("lesson*.json"))
    print(f"Файлов: {len(files)}")

    # Первый проход — читаем все
    data_by_file = {}
    title_srcs = []
    module_srcs = []
    title_keys = []
    module_keys = []

    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        data_by_file[f] = d
        # title.ru
        t_ru = (d.get("title") or {}).get("ru") or (d.get("title") or {}).get("en") or ""
        title_srcs.append(t_ru)
        title_keys.append(f"{f.name}:title")
        # module_title.ru
        m_ru = (d.get("module_title") or {}).get("ru") or (d.get("module_title") or {}).get("en") or ""
        module_srcs.append(m_ru)
        module_keys.append(f"{f.name}:module")

    # 2. Для каждого языка — переводим
    new_titles = {lang: [""] * len(files) for lang in LANGS}
    new_modules = {lang: [""] * len(files) for lang in LANGS}

    for lang in LANGS:
        print(f"\n=== {lang} ===")
        # titles
        print(f"  перевод {len(title_srcs)} title…", end="", flush=True)
        try:
            tr = api(title_srcs, lang)
            if isinstance(tr, list) and len(tr) == len(title_srcs):
                new_titles[lang] = tr
                print(" OK")
            else:
                print(f" !! неверный размер: {len(tr) if isinstance(tr, list) else 'not list'}")
        except Exception as e:
            print(f" !! {e}")
        time.sleep(0.3)

        # module titles
        print(f"  перевод {len(module_srcs)} module_title…", end="", flush=True)
        try:
            tr = api(module_srcs, lang)
            if isinstance(tr, list) and len(tr) == len(module_srcs):
                new_modules[lang] = tr
                print(" OK")
            else:
                print(f" !! неверный размер")
        except Exception as e:
            print(f" !! {e}")
        time.sleep(0.3)

    # 3. Записываем обратно
    print("\n=== запись ===")
    for i, f in enumerate(files):
        d = data_by_file[f]
        for lang in LANGS:
            tv = new_titles[lang][i]
            if tv:
                d.setdefault("title", {})[lang] = tv
            mv = new_modules[lang][i]
            if mv:
                d.setdefault("module_title", {})[lang] = mv
        bak = f.with_suffix(f.suffix + ".pre_titles.bak")
        if not bak.exists():
            shutil.copy2(f, bak)
        f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  {f.name}: title.uz='{d['title'].get('uz','')[:40]}'  module.uz='{d['module_title'].get('uz','')[:40]}'")

    print(f"\nOK: обновлено {len(files)} файлов")
    print("Бэкапы: *.pre_titles.bak")


if __name__ == "__main__":
    main()