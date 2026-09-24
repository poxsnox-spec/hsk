#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fill_grammar.py - merge incoming batch into _grammar/source.json.

Ispolzovanie:
  1. Sozdat _grammar/incoming.json s soderzhimym partii.
  2. Zapustit: py fill_grammar.py
  3. Zatem: py update_grammar.py apply
"""
import json
from pathlib import Path
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
GRAMMAR_DIR = ROOT / "_grammar"
SOURCE = GRAMMAR_DIR / "source.json"
INCOMING = GRAMMAR_DIR / "incoming.json"
LANGS = ["ru", "en", "uz", "tg", "tk"]


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")


def deep_merge(base, patch):
    if isinstance(base, dict) and isinstance(patch, dict):
        for k, v in patch.items():
            if k in base:
                base[k] = deep_merge(base[k], v)
            else:
                base[k] = v
        return base
    return patch


def main():
    if not SOURCE.exists():
        print("Net %s. Snachala: py update_grammar.py extract" % SOURCE)
        sys.exit(1)
    if not INCOMING.exists():
        print("Net %s. Sozdaj ego s soderzhimym partii." % INCOMING)
        sys.exit(1)

    src = load(SOURCE)
    inc = load(INCOMING)

    if "points" not in inc:
        print("incoming.json dolzhen soderzhat klyuch 'points'")
        sys.exit(1)

    patched = 0
    for pid, patch in inc["points"].items():
        if pid not in src["points"]:
            print("!! net tochki: %s" % pid)
            continue
        src["points"][pid] = deep_merge(src["points"][pid], patch)
        patched += 1

    save(SOURCE, src)
    print("OK: obnovleno %d tochek v source.json" % patched)
    print("Dalshe: py update_grammar.py check")
    print("        py update_grammar.py apply --dry-run")
    print("        py update_grammar.py apply")


if __name__ == "__main__":
    main()