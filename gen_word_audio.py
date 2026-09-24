# -*- coding: utf-8 -*-
"""Генерирует mp3 для каждого слова через edge-tts (Microsoft)."""
import asyncio
import json
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("Установи: py -m pip install edge-tts")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
LESSONS = ROOT / "data" / "lessons"
OUT = ROOT / "data" / "audio" / "words"
OUT.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"   # женский нейроголос Microsoft
RATE  = "-15%"                    # чуть медленнее для учебного контекста

def collect_words() -> set:
    words = set()
    for f in sorted(LESSONS.rglob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for w in data.get("vocabulary", []) or []:
            h = (w.get("hanzi") or "").strip()
            if h:
                words.add(h)
        exp = data.get("expansion", {}) or {}
        for w in exp.get("words", []) or []:
            h = (w.get("hanzi") or "").strip()
            if h:
                words.add(h)
    return words

async def synth_one(text: str, path: Path) -> bool:
    if path.exists() and path.stat().st_size > 0:
        return True
    try:
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
        await communicate.save(str(path))
        return True
    except Exception as e:
        print(f"  ! {text!r}: {e}")
        return False

async def main():
    words = collect_words()
    print(f"Найдено слов: {len(words)}")
    print(f"Папка: {OUT}")
    print()
    done = 0
    failed = 0
    for i, hanzi in enumerate(sorted(words), 1):
        fname = OUT / f"{hanzi}.mp3"
        ok = await synth_one(hanzi, fname)
        if ok:
            done += 1
            if i % 50 == 0 or i == len(words):
                print(f"  [{i}/{len(words)}] последнее: {hanzi}  OK")
        else:
            failed += 1
    print()
    print(f"Готово: {done} файлов, ошибок: {failed}")
    total = sum(f.stat().st_size for f in OUT.glob("*.mp3"))
    print(f"Размер: {total / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    asyncio.run(main())