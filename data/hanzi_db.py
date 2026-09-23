# -*- coding: utf-8 -*-
"""Мини-база для анализатора иероглифов Урока 1."""

HANZI_DB = {
    "细": {"radical": "纟", "radical_ru": "нить",     "strokes": 8,  "components": ["纟", "田"]},
    "电": {"radical": "乙", "radical_ru": "изгиб",    "strokes": 5,  "components": ["田", "乚"]},
    "恩": {"radical": "心", "radical_ru": "сердце",   "strokes": 10, "components": ["因", "心"]},
    "对": {"radical": "寸", "radical_ru": "мера",     "strokes": 5,  "components": ["又", "寸"]},
    "入": {"radical": "入", "radical_ru": "входить",  "strokes": 2,  "components": ["入"]},
    "评": {"radical": "讠", "radical_ru": "речь",     "strokes": 7,  "components": ["讠", "平"]},
    "如": {"radical": "女", "radical_ru": "женщина",  "strokes": 6,  "components": ["女", "口"]},
    "瘫": {"radical": "疒", "radical_ru": "болезнь",  "strokes": 15, "components": ["疒", "難"]},
    "离": {"radical": "亠", "radical_ru": "крышка",   "strokes": 10, "components": ["亠", "离"]},
    "自": {"radical": "自", "radical_ru": "сам",      "strokes": 6,  "components": ["自"]},
    "抱": {"radical": "扌", "radical_ru": "рука",     "strokes": 8,  "components": ["扌", "包"]},
    "爱": {"radical": "爪", "radical_ru": "коготь",   "strokes": 10, "components": ["爫", "冖", "友"]},
    "婚": {"radical": "女", "radical_ru": "женщина",  "strokes": 11, "components": ["女", "昏"]},
    "吵": {"radical": "口", "radical_ru": "рот",      "strokes": 7,  "components": ["口", "少"]},
    "相": {"radical": "目", "radical_ru": "глаз",     "strokes": 9,  "components": ["木", "目"]},
    "暗": {"radical": "日", "radical_ru": "солнце",   "strokes": 13, "components": ["日", "音"]},
    "轮": {"radical": "车", "radical_ru": "телега",   "strokes": 8,  "components": ["车", "仑"]},
    "不": {"radical": "一", "radical_ru": "один",     "strokes": 4,  "components": ["一", "不"]},
    "靠": {"radical": "非", "radical_ru": "не",       "strokes": 15, "components": ["告", "非"]},
    "肩": {"radical": "月", "radical_ru": "луна",     "strokes": 8,  "components": ["户", "月"]},
    "喊": {"radical": "口", "radical_ru": "рот",      "strokes": 12, "components": ["口", "咸"]},
    "伸": {"radical": "亻", "radical_ru": "человек",  "strokes": 7,  "components": ["亻", "申"]},
    "手": {"radical": "手", "radical_ru": "рука",     "strokes": 4,  "components": ["手"]},
    "歪": {"radical": "止", "radical_ru": "стопа",    "strokes": 9,  "components": ["不", "正"]},
    "递": {"radical": "辶", "radical_ru": "идти",     "strokes": 10, "components": ["辶", "弟"]},
    "脑": {"radical": "月", "radical_ru": "луна",     "strokes": 10, "components": ["月", "文", "凵"]},
    "女": {"radical": "女", "radical_ru": "женщина",  "strokes": 3,  "components": ["女"]},
    "叙": {"radical": "又", "radical_ru": "снова",    "strokes": 9,  "components": ["余", "又"]},
    "居": {"radical": "尸", "radical_ru": "тело",     "strokes": 8,  "components": ["尸", "古"]},
    "催": {"radical": "亻", "radical_ru": "человек",  "strokes": 13, "components": ["亻", "崔"]},
    "等": {"radical": "竹", "radical_ru": "бамбук",   "strokes": 12, "components": ["竹", "寺"]},
    "蚊": {"radical": "虫", "radical_ru": "насекомое","strokes": 10, "components": ["虫", "文"]},
    "半": {"radical": "十", "radical_ru": "десять",   "strokes": 5,  "components": ["八", "十"]},
    "叮": {"radical": "口", "radical_ru": "рот",      "strokes": 5,  "components": ["口", "丁"]},
    "老": {"radical": "老", "radical_ru": "старый",   "strokes": 6,  "components": ["老"]},
    "吵": {"radical": "口", "radical_ru": "рот",      "strokes": 7,  "components": ["口", "少"]},
}


def analyze(hanzi: str):
    if not hanzi:
        return None
    first = hanzi[0]
    return HANZI_DB.get(first)


def split_pinyin(pinyin: str):
    """Разбирает пиньинь на слоги с указанием тона."""
    TONE_MAP = {
        "ā": ("a", 1), "á": ("a", 2), "ǎ": ("a", 3), "à": ("a", 4),
        "ē": ("e", 1), "é": ("e", 2), "ě": ("e", 3), "è": ("e", 4),
        "ī": ("i", 1), "í": ("i", 2), "ǐ": ("i", 3), "ì": ("i", 4),
        "ō": ("o", 1), "ó": ("o", 2), "ǒ": ("o", 3), "ò": ("o", 4),
        "ū": ("u", 1), "ú": ("u", 2), "ǔ": ("u", 3), "ù": ("u", 4),
        "ǖ": ("ü", 1), "ǘ": ("ü", 2), "ǚ": ("ü", 3), "ǜ": ("ü", 4),
    }
    result = []
    for raw_syl in pinyin.strip().split():
        tone = 5
        plain = raw_syl
        for ch, (base, t) in TONE_MAP.items():
            if ch in raw_syl:
                plain = raw_syl.replace(ch, base)
                tone = t
                break
        result.append({"syl": plain, "tone": tone, "display": raw_syl})
    return result


TONE_NAMES = {
    1: {"ru": "1-й тон (ровный)",     "tk": "1-nji ton (deň)",      "en": "1st tone (level)"},
    2: {"ru": "2-й тон (восходящий)", "tk": "2-nji ton (ýokary)",   "en": "2nd tone (rising)"},
    3: {"ru": "3-й тон (низкий)",     "tk": "3-nji ton (aşaky)",    "en": "3rd tone (dipping)"},
    4: {"ru": "4-й тон (падающий)",   "tk": "4-nji ton (aşak)",     "en": "4th tone (falling)"},
    5: {"ru": "Нейтральный тон",      "tk": "Neytral ton",           "en": "Neutral tone"},
}