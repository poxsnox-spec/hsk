#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Парсит HSK6 PDF -> words.json (сырые данные, чистка через DeepSeek)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "hsk6_data" / "HSK-6-Vocabulary.pdf"
RAW_PATH = ROOT / "hsk6_data" / "raw.txt"
OUT = ROOT / "hsk6_data" / "words.json"

LINE_RE = re.compile(
    r'^\s*(\d{1,4})\s+'
    r'([\u4e00-\u9fff\u3007]{1,10})\s+'
    r'([A-Za-z\u0100-\u01FF\u1E00-\u1EFF\u00C0-\u00FF\s]+?)\s+'
    r'(.+?)\s*$'
)
GARBAGE_HANZI = {"\u4e19", "\u4e01", "\u752c"}


def extract_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            print("!! pip install pypdf")
            sys.exit(1)
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def parse(text):
    words, seen = [], set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("=") or line.startswith("Page"):
            continue
        m = LINE_RE.match(line)
        if not m:
            continue
        num_s, hanzi, pinyin, eng = m.groups()
        try:
            num = int(num_s)
        except ValueError:
            continue
        if num in seen or hanzi in GARBAGE_HANZI:
            continue
        seen.add(num)
        words.append({
            "id": num,
            "hanzi": hanzi,
            "pinyin_raw": pinyin.strip(),
            "english_raw": eng.strip(),
        })
    words.sort(key=lambda w: w["id"])
    for i, w in enumerate(words, 1):
        w["id"] = i
    return words


def main():
    if PDF_PATH.exists():
        print("Читаю PDF:", PDF_PATH.name)
        text = extract_pdf(PDF_PATH)
    elif RAW_PATH.exists():
        print("Читаю:", RAW_PATH.name)
        text = RAW_PATH.read_text(encoding="utf-8")
    else:
        print("!! Нет", PDF_PATH.name, "и", RAW_PATH.name)
        sys.exit(1)

    words = parse(text)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK:", len(words), "слов ->", OUT)


if __name__ == "__main__":
    main()