# -*- coding: utf-8 -*-
"""Модели данных урока — включая материалы из рабочей тетради."""
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any
from core.config import LESSONS_DIR


@dataclass
class VocabEntry:
    hanzi: str
    pinyin: str
    pos: str
    meaning: Dict[str, str]
    audio: str = ""

    def translate(self, lang: str) -> str:
        return self.meaning.get(lang) or self.meaning.get("en", "")


@dataclass
class GrammarPoint:
    word: str
    pos: str
    explanation: Dict[str, str]
    examples: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class ComparePoint:
    word_a: str
    word_b: str
    common: Dict[str, str]
    differences: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class QuizQuestion:
    type: str
    prompt: Dict[str, str]
    options: List[str] = field(default_factory=list)
    answer: Any = None
    audio: str = ""
    explanation: Dict[str, str] = field(default_factory=dict)


@dataclass
class Lesson:
    lesson_id: str
    unit: int
    index: int
    title: Dict[str, str]

    warmup: Dict[str, Any] = field(default_factory=dict)
    text_zh: str = ""
    text_translation: Dict[str, str] = field(default_factory=dict)
    vocabulary: List[VocabEntry] = field(default_factory=list)
    grammar: List[GrammarPoint] = field(default_factory=list)
    collocations: List[Dict[str, Any]] = field(default_factory=list)
    comparisons: List[ComparePoint] = field(default_factory=list)
    expansion: Dict[str, Any] = field(default_factory=dict)
    application: Dict[str, Any] = field(default_factory=dict)

    wb_listening: List[QuizQuestion] = field(default_factory=list)
    wb_reading:   List[QuizQuestion] = field(default_factory=list)
    wb_writing:   List[Dict[str, Any]] = field(default_factory=list)

    audio_files: Dict[str, str] = field(default_factory=dict)

    def title_in(self, lang: str) -> str:
        return self.title.get(lang) or self.title.get("en") or self.title.get("zh", "")


_LESSON_CACHE: dict = {}


def clear_cache():
    _LESSON_CACHE.clear()


def load_lesson(unit: int, index: int) -> Lesson:
    key = (unit, index)
    if key in _LESSON_CACHE:
        return _LESSON_CACHE[key]
    lesson = _load_lesson_uncached(unit, index)
    _LESSON_CACHE[key] = lesson
    return lesson


def _load_lesson_uncached(unit: int, index: int) -> Lesson:
    path = LESSONS_DIR / f"unit{unit}" / f"lesson{index:02d}.json"
    if not path.exists():
        raise FileNotFoundError(f"Файл урока не найден: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    vocab = [
        VocabEntry(
            hanzi=w["hanzi"], pinyin=w["pinyin"],
            pos=w.get("pos", ""), meaning=w.get("meaning", {}),
            audio=w.get("audio", ""),
        )
        for w in raw.get("vocabulary", [])
    ]
    grammar = [
        GrammarPoint(word=g["word"], pos=g.get("pos", ""),
                     explanation=g.get("explanation", {}),
                     examples=g.get("examples", []))
        for g in raw.get("grammar", [])
    ]
    comparisons = [
        ComparePoint(word_a=c["word_a"], word_b=c["word_b"],
                     common=c.get("common", {}),
                     differences=c.get("differences", []))
        for c in raw.get("comparisons", [])
    ]

    def _to_quiz(lst):
        return [
            QuizQuestion(
                type=q.get("type", "mc"),
                prompt=q.get("prompt", {}),
                options=q.get("options", []),
                answer=q.get("answer"),
                audio=q.get("audio", ""),
                explanation=q.get("explanation", {}),
            )
            for q in lst
        ]

    return Lesson(
        lesson_id=f"unit{unit}_lesson{index}",
        unit=unit, index=index,
        title=raw.get("title", {}),
        warmup=raw.get("warmup", {}),
        text_zh=raw.get("text_zh", ""),
        text_translation=raw.get("text_translation", {}),
        vocabulary=vocab,
        grammar=grammar,
        collocations=raw.get("collocations", []),
        comparisons=comparisons,
        expansion=raw.get("expansion", {}),
        application=raw.get("application", {}),
        wb_listening=_to_quiz(raw.get("workbook", {}).get("listening", [])),
        wb_reading=_to_quiz(raw.get("workbook", {}).get("reading", [])),
        wb_writing=raw.get("workbook", {}).get("writing", []),
        audio_files=raw.get("audio_files", {}),
    )