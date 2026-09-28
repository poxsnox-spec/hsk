#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заполняет .en для title/module_title у уроков 2-15."""
import json, os, sys, time, shutil
from pathlib import Path
import requests

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY","") if 32 < ord(c) < 127)
if not API_KEY:
    print("!! нет DEEPSEEK_API_KEY"); sys.exit(1)

BASE = "https://api.deepseek.com/chat/completions"
BIZ = Path("data/business")


def api(items):
    lines = [
        "Translate each string into English. Source is Russian.",
        "These are titles of business Chinese textbook lessons. Keep concise, natural.",
        "Return JSON array of translations in SAME order.",
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
    files = sorted(BIZ.glob("lesson*.json"))
    print(f"Файлов: {len(files)}")

    title_tasks, title_idx = [], []
    mod_tasks, mod_idx = [], []
    data_by_file = {}

    for i, f in enumerate(files):
        d = json.loads(f.read_text(encoding="utf-8"))
        data_by_file[f] = d
        t = d.get("title") or {}
        if not (t.get("en") or "").strip() and (t.get("ru") or "").strip():
            title_tasks.append(t["ru"]); title_idx.append(i)
        m = d.get("module_title") or {}
        if not (m.get("en") or "").strip() and (m.get("ru") or "").strip():
            mod_tasks.append(m["ru"]); mod_idx.append(i)

    print(f"  title без en:        {len(title_tasks)}")
    print(f"  module_title без en: {len(mod_tasks)}")

    title_en = [""] * len(files)
    mod_en = [""] * len(files)

    if title_tasks:
        print(f"\nПеревожу {len(title_tasks)} title…", end="", flush=True)
        try:
            tr = api(title_tasks)
            if isinstance(tr, list) and len(tr) == len(title_tasks):
                for k, i in enumerate(title_idx):
                    title_en[i] = tr[k]
                print(" OK")
            else:
                print(f" !! неверный размер")
        except Exception as e:
            print(f" !! {e}")
        time.sleep(0.3)

    if mod_tasks:
        print(f"Перевожу {len(mod_tasks)} module_title…", end="", flush=True)
        try:
            tr = api(mod_tasks)
            if isinstance(tr, list) and len(tr) == len(mod_tasks):
                for k, i in enumerate(mod_idx):
                    mod_en[i] = tr[k]
                print(" OK")
            else:
                print(f" !! неверный размер")
        except Exception as e:
            print(f" !! {e}")

    print("\n=== запись ===")
    for i, f in enumerate(files):
        d = data_by_file[f]
        if title_en[i]:
            d.setdefault("title", {})["en"] = title_en[i]
        if mod_en[i]:
            d.setdefault("module_title", {})["en"] = mod_en[i]
        bak = f.with_suffix(f.suffix + ".pre_en.bak")
        if not bak.exists():
            shutil.copy2(f, bak)
        f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        en = d["title"].get("en", "")
        mn = d["module_title"].get("en", "")
        print(f"  {f.name}: title.en='{en[:45]}'  module.en='{mn[:35]}'")

    print(f"\nOK: обновлено {len(files)} файлов")


if __name__ == "__main__":
    main()