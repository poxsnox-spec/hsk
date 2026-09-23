# -*- coding: utf-8 -*-
"""Единый набор плоских иконок через Segoe Fluent Icons."""
from PyQt5.QtGui import QFont, QFontDatabase


# Segoe Fluent Icons (Windows 11 / Windows 10 1809+)
# Fallback: Segoe MDL2 Assets (Windows 10 старые)
# Fallback: Unicode-символы (всегда работают)

ICON_CODES = {
    # Левое меню
    "lessons":   "\uE8F1",   # Library / books
    "vocab":     "\uE8A5",   # Document
    "srs":       "\uE895",   # Sync
    "heatmap":   "\uE9D2",   # BarChart
    "stats":     "\uE9D9",   # Analytics (line)
    "analyzer":  "\uE721",   # Search
    # Правая панель
    "language":  "\uE774",   # Globe
    "theme":     "\uE706",   # Sun
    "settings":  "\uE713",   # Settings (gear)
    "about":     "\uE946",   # Info
    "chevron":   "\uE76C",   # Chevron right
    "play":      "\uE768",   # Play
    "streak":    "\uE9F0",   # Fire
    "check":     "\uE73E",   # Checkmark
}

# Резервные Unicode-символы (если Fluent нет в системе)
FALLBACK = {
    "lessons":   "\u25A4",  "vocab":     "\u25A5",
    "srs":       "\u21BB",  "heatmap":   "\u2261",
    "stats":     "\u2197",  "analyzer":  "\u2315",
    "language":  "\u25CB",  "theme":     "\u2600",
    "settings":  "\u2699",  "about":     "\u24D8",
    "chevron":   "\u203A",  "play":      "\u25B6",
    "streak":    "\u2605",  "check":     "\u2713",
}


def get_icon_font(size: int) -> QFont:
    """Возвращает QFont с иконками."""
    try:
        families = set(QFontDatabase().families())
    except Exception:
        families = set()
    for name in ("Segoe Fluent Icons", "Segoe MDL2 Assets"):
        if name in families:
            return QFont(name, size)
    return QFont("Segoe UI Symbol", size)


def icon(name: str) -> str:
    """Возвращает код иконки по имени."""
    try:
        families = set(QFontDatabase().families())
    except Exception:
        families = set()
    has_fluent = ("Segoe Fluent Icons" in families
                  or "Segoe MDL2 Assets" in families)
    if has_fluent:
        return ICON_CODES.get(name, "?")
    return FALLBACK.get(name, "?")
