#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Вырезает диалоги и словарь из mp3 через ffmpeg (без перекодирования)."""
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SRC = Path(r"C:\Users\poxsn\OneDrive\Desktop\sss\商务中文01-1.mp3")

# Куда сохранить
DST_DIR = Path("data/audio/business/lesson01")

# ⚠️ Поправь таймкоды после прослушивания, если нужно
# (format: start_sec, end_sec, filename)
CUTS = [
    (0.0,   82.0, "dialog_airport.mp3"),
    (82.0, 152.0, "dialog_hotel.mp3"),
    (152.0, 203.0, "vocab.mp3"),
]


def main():
    if not SRC.exists():
        print(f"!! нет файла: {SRC}")
        return

    DST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Источник: {SRC}")
    print(f"Размер: {SRC.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"Куда: {DST_DIR.resolve()}")
    print()

    for start, end, name in CUTS:
        out = DST_DIR / name
        dur = end - start
        print(f"  {start:>6.1f} → {end:>6.1f} ({dur:>5.1f} сек) → {name}…", end="", flush=True)

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", str(SRC),
            "-t", str(dur),
            "-c", "copy",       # без перекодирования
            "-loglevel", "error",
            str(out),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f" !! ошибка: {r.stderr[:200]}")
            continue
        size = out.stat().st_size / 1024
        print(f" OK ({size:.0f} KB)")

    print()
    print("Готово. Проверь файлы:")
    for _, _, name in CUTS:
        f = DST_DIR / name
        if f.exists():
            print(f"  ✓ {name}  {f.stat().st_size/1024:.0f} KB")
        else:
            print(f"  ✗ {name}  (нет)")


if __name__ == "__main__":
    main()