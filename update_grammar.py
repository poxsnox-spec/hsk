#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_grammar.py - obnovlenie razdela grammatiki HSK5 cherez cmd.

Komandy:
  py update_grammar.py extract          # sobrat vse tochki v _grammar/source.json
  py update_grammar.py extract --one unit1/lesson01
  py update_grammar.py apply            # zalit source.json obratno v uroki
  py update_grammar.py apply --dry-run  # posmotret chto budet izmeneno
  py update_grammar.py check            # proverit zapolnenie
  py update_grammar.py stats            # statistika
  py update_grammar.py new --unit 1 --lesson 1 --word 如何 --pos pron.
  py update_grammar.py show unit1_lesson01_g0
"""

import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
LESSONS_DIR = ROOT / "data" / "lessons"
GRAMMAR_DIR = ROOT / "_grammar"
SOURCE_FILE = GRAMMAR_DIR / "source.json"

LANGS = ["ru", "en", "uz", "tg", "tk"]

CORE_FIELDS = ["word", "pos"]
OLD_FIELDS  = ["explanation", "examples"]
NEW_FIELDS  = ["formula", "when_to_use", "common_mistakes", "comparison_with", "exercises"]
ALL_FIELDS  = CORE_FIELDS + OLD_FIELDS + NEW_FIELDS


def parse_lesson_path(p):
    unit = int(p.parent.name.replace("unit", ""))
    lesson = int(p.stem.replace("lesson", ""))
    return unit, lesson


def iter_lessons(one_filter=None):
    for f in sorted(LESSONS_DIR.rglob("lesson*.json")):
        if ".bak" in f.name or ".pre_" in f.name:
            continue
        if one_filter:
            rel = f.parent.name + "/" + f.stem
            if rel != one_filter.replace("\\", "/"):
                continue
        yield f


def make_id(unit, lesson, idx):
    return "unit%d_lesson%02d_g%d" % (unit, lesson, idx)


def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")


def backup(p, suffix):
    bak = p.with_suffix(p.suffix + suffix)
    if not bak.exists():
        shutil.copy2(p, bak)


def empty_lang_str():
    return {l: "" for l in LANGS}


def empty_lang_list():
    return {l: [] for l in LANGS}


def cmd_extract(args):
    GRAMMAR_DIR.mkdir(exist_ok=True)
    source = {
        "_meta": {
            "version": 2,
            "created": datetime.datetime.now().isoformat(timespec="seconds"),
            "languages": LANGS,
            "schema": {
                "word": "ieroglif/konstrukciya",
                "pos": "chast rechi",
                "explanation": "{ru,en,uz,tg,tk} bazovoe obyasnenie",
                "formula": "{lang} formula/shema",
                "when_to_use": "{lang: [stroka,...]} kogda upotreblyaetsya",
                "examples": "[{zh, ru, en, uz, tg, tk, note?}]",
                "common_mistakes": "[{wrong, right, why:{lang}}]",
                "comparison_with": "[{word, difference:{lang}}]",
                "exercises": "[{type, question, answer}]",
            },
        },
        "points": {},
    }

    total = 0
    files = 0
    for f in iter_lessons(args.one):
        files += 1
        unit, lesson = parse_lesson_path(f)
        data = load_json(f)
        for idx, g in enumerate(data.get("grammar") or []):
            pid = make_id(unit, lesson, idx)
            entry = {
                "unit": unit,
                "lesson": lesson,
                "index": idx,
                "file": str(f.relative_to(ROOT)).replace("\\", "/"),
            }
            for k in ALL_FIELDS:
                if k in g and g[k] not in (None, "", [], {}):
                    entry[k] = g[k]
            entry.setdefault("word", g.get("word", ""))
            entry.setdefault("pos",  g.get("pos", ""))
            entry.setdefault("explanation", empty_lang_str())
            entry.setdefault("formula",     empty_lang_str())
            entry.setdefault("when_to_use", empty_lang_list())
            entry.setdefault("examples",        [])
            entry.setdefault("common_mistakes", [])
            entry.setdefault("comparison_with", [])
            entry.setdefault("exercises",       [])
            source["points"][pid] = entry
            total += 1

    save_json(SOURCE_FILE, source)
    print("OK: %d tochek iz %d urokov" % (total, files))
    print("Fajl: %s" % SOURCE_FILE)
    print("Dalshe: otredaktiruj source.json i zapusti: py update_grammar.py apply")


def cmd_apply(args):
    if not SOURCE_FILE.exists():
        print("Net fajla %s. Snachala: py update_grammar.py extract" % SOURCE_FILE)
        sys.exit(1)

    src = load_json(SOURCE_FILE)
    by_file = {}
    for pid, entry in src["points"].items():
        by_file.setdefault(entry["file"], []).append((pid, entry))

    changed_files = 0
    changed_points = 0

    for rel, items in by_file.items():
        f = ROOT / rel
        if not f.exists():
            print("!! net fajla: %s" % rel)
            continue
        data = load_json(f)
        grammar = data.get("grammar") or []
        touched = False
        for pid, entry in items:
            idx = entry["index"]
            if idx >= len(grammar):
                print("!! %s: indeks %d vne diapazona (%d)" % (pid, idx, len(grammar)))
                continue
            g = grammar[idx]
            for k in ALL_FIELDS:
                if k in entry and entry[k] not in (None, "", [], {}):
                    g[k] = entry[k]
            changed_points += 1
            touched = True
        if touched:
            if not args.dry_run:
                backup(f, ".pre_grammar_update.bak")
                save_json(f, data)
            changed_files += 1
            prefix = "  [dry] " if args.dry_run else "  OK    "
            print(prefix + rel)

    tag = "DRY-RUN: " if args.dry_run else ""
    print("\n%sobnovleno %d fajlov, %d tochek" % (tag, changed_files, changed_points))


def cmd_check(args):
    src = load_json(SOURCE_FILE)
    problems = []
    for pid, e in src["points"].items():
        expl = e.get("explanation") or {}
        for l in LANGS:
            if not (expl.get(l) or "").strip():
                problems.append("%s: pusto explanation.%s" % (pid, l))
        if not e.get("examples"):
            problems.append("%s: net examples" % pid)
        else:
            for i, ex in enumerate(e["examples"]):
                if not ex.get("zh"):
                    problems.append("%s: examples[%d].zh pust" % (pid, i))
                for l in LANGS:
                    if not (ex.get(l) or "").strip():
                        problems.append("%s: examples[%d].%s pust" % (pid, i, l))
        fm = e.get("formula") or {}
        if not any((fm.get(l) or "").strip() for l in LANGS):
            problems.append("%s: net formula" % pid)
        wtu = e.get("when_to_use") or {}
        if not any(wtu.get(l) for l in LANGS):
            problems.append("%s: pustoj when_to_use" % pid)

    if not problems:
        print("OK: vse tochki zapolneny")
        return
    print("Najdeno %d problem:" % len(problems))
    for p in problems[:200]:
        print("  -", p)
    if len(problems) > 200:
        print("  ... eshe %d" % (len(problems) - 200))


def cmd_stats(args):
    src = load_json(SOURCE_FILE)
    pts = src["points"]
    n = len(pts)
    print("Tochek: %d" % n)
    print("Yazykov: %s" % ", ".join(LANGS))
    print()
    print("%-20s%12s" % ("pole", "zapolneno"))
    for field in ["explanation", "formula", "when_to_use", "examples",
                  "common_mistakes", "comparison_with", "exercises"]:
        cnt = 0
        for e in pts.values():
            v = e.get(field)
            if isinstance(v, dict):
                if any((v.get(l) or "") for l in LANGS):
                    cnt += 1
            elif v:
                cnt += 1
        print("%-20s%6d / %d" % (field, cnt, n))
    print()
    from collections import Counter
    c = Counter((e["unit"], e["lesson"]) for e in pts.values())
    for (u, l), k in sorted(c.items()):
        print("  unit%d/lesson%02d: %d" % (u, l, k))


def cmd_new(args):
    if not SOURCE_FILE.exists():
        cmd_extract(argparse.Namespace(one=None))
    src = load_json(SOURCE_FILE)
    same = [e for e in src["points"].values()
            if e["unit"] == args.unit and e["lesson"] == args.lesson]
    idx = len(same)
    pid = make_id(args.unit, args.lesson, idx)
    file_rel = "data/lessons/unit%d/lesson%02d.json" % (args.unit, args.lesson)
    src["points"][pid] = {
        "unit": args.unit, "lesson": args.lesson, "index": idx,
        "file": file_rel,
        "word": args.word, "pos": args.pos or "",
        "explanation": empty_lang_str(),
        "formula":     empty_lang_str(),
        "when_to_use": empty_lang_list(),
        "examples": [], "common_mistakes": [],
        "comparison_with": [], "exercises": [],
    }
    save_json(SOURCE_FILE, src)
    print("Dobavlena zagotovka: %s" % pid)


def cmd_show(args):
    src = load_json(SOURCE_FILE)
    e = src["points"].get(args.id)
    if not e:
        print("Ne najdeno: %s" % args.id)
        return
    print(json.dumps(e, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Obnovlenie grammatiki HSK5")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("extract")
    p.add_argument("--one", default=None)
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("apply")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_apply)

    p = sub.add_parser("check")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("stats")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("new")
    p.add_argument("--unit", type=int, required=True)
    p.add_argument("--lesson", type=int, required=True)
    p.add_argument("--word", required=True)
    p.add_argument("--pos", default="")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("show")
    p.add_argument("id")
    p.set_defaults(func=cmd_show)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()