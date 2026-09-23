# -*- coding: utf-8 -*-
"""HSK 5 Learner — точка входа (HiDPI-aware)."""
import ctypes
import sys

# === DPI AWARENESS — ДО import tkinter ===
if sys.platform == "win32":
    try:
        # Per-monitor v2 (Windows 10+)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

import tkinter as tk

from core.config import (APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT,
                         WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
from core.theme import theme
from core.i18n import i18n
from core.storage import storage
from core.screen_manager import ScreenManager

from ui.screens.language_select import LanguageSelectScreen
from ui.screens.main_menu import MainMenuScreen
from ui.screens.lesson_menu import LessonMenuScreen
from ui.screens.lesson_view import LessonViewScreen
from ui.screens.flashcard_screen import FlashcardScreen
from ui.screens.exercise_screen import ExerciseScreen
from ui.screens.trainer_screen import TrainerScreen
from ui.screens.analyzer_screen import AnalyzerScreen
from ui.screens.writing_screen import WritingScreen
from ui.screens.stats_screen import StatsScreen
from ui.screens.vocab_screen import VocabScreen
from ui.screens.srs_screen import SrsScreen
from ui.screens.heatmap_screen import HeatmapScreen


def get_dpi_scale(root):
    """Возвращает коэффициент масштаба (1.0 = 96 dpi / 100%)."""
    try:
        dpi = root.winfo_fpixels("1i")  # пикселей в одном дюйме
        return max(1.0, dpi / 96.0)
    except Exception:
        return 1.0


def main():
    root = tk.Tk()
    root.title(APP_NAME)

    # --- Масштабирование Tkinter ---
    scale = get_dpi_scale(root)
    # Сохраняем в теме — используется для шрифтов
    theme.init(dpi_scale=scale)

    # Окно — увеличиваем пропорционально DPI
    w = int(WINDOW_WIDTH * scale)
    h = int(WINDOW_HEIGHT * scale)
    min_w = int(WINDOW_MIN_WIDTH * scale)
    min_h = int(WINDOW_MIN_HEIGHT * scale)

    # Не даём окну вылезти за пределы экрана
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    w = min(w, sw - 40)
    h = min(h, sh - 80)

    root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
    root.minsize(min_w, min_h)
    root.configure(bg=theme.c("bg"))

    # Tkinter scaling для размеров виджетов (padx, width в символах и т.д.)
    try:
        root.tk.call("tk", "scaling", scale)
    except Exception:
        pass

    i18n.set_language(storage.get("language", "ru"))
    theme.set_mode(storage.get("theme_mode", "light"))

    container = tk.Frame(root, bg=theme.c("bg"))
    container.pack(fill="both", expand=True)

    manager = ScreenManager(container)
    manager.register("language_select", LanguageSelectScreen)
    manager.register("main_menu",       MainMenuScreen)
    manager.register("lessons",         LessonMenuScreen)
    manager.register("lesson_view",     LessonViewScreen)
    manager.register("flashcards",      FlashcardScreen)
    manager.register("exercise",        ExerciseScreen)
    manager.register("trainer",         TrainerScreen)
    manager.register("analyzer",        AnalyzerScreen)
    manager.register("writing",         WritingScreen)
    manager.register("stats",           StatsScreen)
    manager.register("vocab",           VocabScreen)
    manager.register("srs",             SrsScreen)
    manager.register("heatmap",         HeatmapScreen)

    manager.show("language_select", push_history=False)
    root.mainloop()


if __name__ == "__main__":
    main()
