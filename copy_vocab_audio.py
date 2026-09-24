# -*- coding: utf-8 -*-
"""Копирует <NN>-2.mp3 как vocab.mp3 в data/audio/<unit>/<lesson>/."""
import shutil
from pathlib import Path

SRC = Path(r"C:\Users\poxsn\OneDrive\Desktop\HSK-5 SB1（上）-AUDIO\HSK标准教程5（上）课本 录音")
DST = Path(__file__).resolve().parent / "data" / "audio"

if not SRC.exists():
    print(f"!! Папка не найдена: {SRC}")
    raise SystemExit(1)

total = 0
total_bytes = 0
missing = []

for n in range(1, 19):
    fname = f"{n:02d}-2.mp3"
    src_file = SRC / fname
    if not src_file.exists():
        missing.append(fname)
        continue

    unit = (n - 1) // 3 + 1
    lesson = (n - 1) % 3 + 1
    dst_dir = DST / f"unit{unit}" / f"lesson{lesson:02d}"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_file = dst_dir / "vocab.mp3"

    shutil.copy2(src_file, dst_file)
    size = dst_file.stat().st_size
    total += 1
    total_bytes += size
    print(f"  {fname}  ->  unit{unit}/lesson{lesson:02d}/vocab.mp3  ({size // 1024} KB)")

print()
print(f"Скопировано: {total} файлов, {total_bytes / 1024 / 1024:.1f} MB")
if missing:
    print(f"НЕ найдено: {missing}")