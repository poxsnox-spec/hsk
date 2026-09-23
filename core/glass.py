# -*- coding: utf-8 -*-
"""Помощник для glass-эффекта: скруглённые карточки + паттерн фона."""

# Декоративные иероглифы и символы для фона
BG_CHARS = "汉字学习研究书道文心画意诗词歌赋"
MATH_CHARS = "xyabf∑∫π√∞θαβΔ"


def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Рисует скруглённый прямоугольник на Canvas."""
    points = [
        x1+r, y1,  x1+r, y1,  x2-r, y1,  x2-r, y1,  x2, y1,
        x2, y1+r,  x2, y1+r,  x2, y2-r,  x2, y2-r,  x2, y2,
        x2-r, y2,  x2-r, y2,  x1+r, y2,  x1+r, y2,  x1, y2,
        x1, y2-r,  x1, y2-r,  x1, y1+r,  x1, y1+r,  x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)
