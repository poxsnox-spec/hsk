# -*- coding: utf-8 -*-
"""Главное окно — без QStackedWidget, экраны полностью пересоздаются."""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QMessageBox,
                             QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from qt.theme import qt_theme
from qt.glass import make_background_pixmap
from qt.screens.language_select import LanguageSelectScreen
from qt.screens.grammar_lib_screen import GrammarLibScreen
from qt.screens.compare_lib_screen import CompareLibScreen
from qt.screens.main_menu import MainMenuScreen
from qt.screens.lesson_menu import LessonMenuScreen
from qt.screens.lesson_view import LessonViewScreen
from qt.screens.exercise_screen import ExerciseScreen
from qt.screens.srs_screen import SrsScreen
from qt.screens.trainer_screen import TrainerScreen
from qt.screens.analyzer_screen import AnalyzerScreen
from qt.screens.heatmap_screen import HeatmapScreen
from qt.screens.stats_screen import StatsScreen
from qt.screens.settings_screen import SettingsScreen
from qt.screens.vocab_screen import VocabScreen
from core.i18n import i18n
from core.storage import storage
from core.config import APP_NAME


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None

    def set_pixmap(self, pm):
        self._pixmap = pm
        self.update()

    def paintEvent(self, event):
        if self._pixmap is None or self._pixmap.isNull():
            return
        p = QPainter(self)
        p.drawPixmap(0, 0, self._pixmap)
        p.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1280, 800)
        self.setMinimumSize(1000, 640)

        # Фон с паттерном
        self.bg_widget = BackgroundWidget()
        self.setCentralWidget(self.bg_widget)

        # Контейнер для экранов (НЕ QStackedWidget — просто слой поверх фона)
        self.container = QWidget(self.bg_widget)
        self.container.setAttribute(Qt.WA_TranslucentBackground, True)

        lay = QVBoxLayout(self.bg_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.container)

        self.container_lay = QVBoxLayout(self.container)
        self.container_lay.setContentsMargins(0, 0, 0, 0)

        self._current = None
        self._last_lesson = None

        self._show_initial()

    # ------------------------------------------------------------
    def _clear_current(self):
        """Полностью удаляет текущий экран из контейнера."""
        if self._current is None:
            return
        try:
            self._current.hide()
            self._current.setVisible(False)
            self._current.setParent(None)
            self._current.deleteLater()
        except Exception as e:
            print(f"[clear] {e}")
        self._current = None
        # Даём Qt время обработать удаление
        QApplication.processEvents()

    def _set_screen(self, widget):
        """Убирает старый экран и ставит новый."""
        self._clear_current()
        self._current = widget
        self._current.setParent(self.container)
        self.container_lay.addWidget(self._current)
        self._current.show()
        self._current.raise_()
        QApplication.processEvents()

    # ------------------------------------------------------------
    def _show_initial(self):
        saved_lang = storage.get("language")
        if saved_lang in ("ru", "tk", "en"):
            i18n.set_language(saved_lang)
            self._show_main_menu()
        else:
            self._show_language_select()

    # ------------------------------------------------------------
    def _show_language_select(self):
        screen = LanguageSelectScreen(self)
        screen.language_selected.connect(self._on_lang_chosen)
        self._set_screen(screen)

    def _on_lang_chosen(self, code):
        self._show_main_menu()

    # ------------------------------------------------------------
    def _show_main_menu(self):
        screen = MainMenuScreen(self)
        screen.open_screen.connect(self._open_screen)
        screen.toggle_theme.connect(self._toggle_theme)
        self._set_screen(screen)

    def _show_lesson_menu(self):
        screen = LessonMenuScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        screen.lesson_open.connect(self._open_lesson)
        self._set_screen(screen)

    def _open_lesson(self, unit, index):
        self._last_lesson = (unit, index)
        screen = LessonViewScreen(unit, index, self)
        screen.back_requested.connect(self._show_lesson_menu)
        screen.exercise_requested = self._open_exercise
        self._set_screen(screen)

    def _open_exercise(self, unit, index, mode):
        self._last_lesson = (unit, index)
        screen = ExerciseScreen(unit, index, mode, self)
        screen.back_requested.connect(self._back_to_lesson)
        self._set_screen(screen)

    def _back_to_lesson(self):
        if self._last_lesson:
            u, i = self._last_lesson
            self._open_lesson(u, i)

    def _show_srs(self):
        screen = SrsScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _show_analyzer(self):
        screen = AnalyzerScreen(1, 1, self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _show_heatmap(self):
        screen = HeatmapScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _show_stats(self):
        screen = StatsScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _show_settings(self):
        screen = SettingsScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        screen.lang_changed.connect(self._on_settings_lang)
        screen.profile_changed.connect(self._on_profile_changed)
        self._set_screen(screen)


    def _on_settings_lang(self):
        self._show_settings()

    # ------------------------------------------------------------
    def _show_vocab(self):
        screen = VocabScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _show_grammar_lib(self):
        screen = GrammarLibScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _show_compare_lib(self):
        screen = CompareLibScreen(self)
        screen.back_requested.connect(self._show_main_menu)
        self._set_screen(screen)

    def _open_screen(self, action):
        mapping = {
            "lessons":  self._show_lesson_menu,
            "vocab":    self._show_vocab,
            "srs":      self._show_srs,
            "analyzer": self._show_analyzer,
            "heatmap":  self._show_heatmap,
            "stats":    self._show_stats,
            "settings": self._show_settings,
            "grammar_lib":  self._show_grammar_lib,
            "compare_lib":  self._show_compare_lib,
        }
        fn = mapping.get(action)
        if fn:
            fn()
        else:
            QMessageBox.information(
                self, "Скоро!",
                f"Экран «{action}» появится позже."
            )

    def _change_lang(self):
        cur = i18n.language
        order = ["ru", "tk", "en"]
        nxt = order[(order.index(cur) + 1) % len(order)]
        i18n.set_language(nxt)
        storage.set("language", nxt)
        self._show_main_menu()

    def _toggle_theme(self):
        new_mode = qt_theme.toggle()
        storage.set("theme_mode", new_mode)
        self._rebuild_background()
        self._show_main_menu()

    def _show_about(self):
        QMessageBox.about(
            self, "About",
            f"<b>{APP_NAME}</b><br><br>"
            "HSK 5 上 · Тренажёр<br>"
            "PyQt5 Liquid Glass"
        )

    # ------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._rebuild_background()

    def _on_profile_changed(self):
        """При смене профиля — пересобираем главное меню."""
        try:
            self._show_main_menu()
        except Exception as e:
            print(f"[profile] error: {e}")

    def _rebuild_background(self):
        w, h = self.width(), self.height()
        if w < 50 or h < 50:
            return
        self.bg_widget.set_pixmap(make_background_pixmap(w, h))
