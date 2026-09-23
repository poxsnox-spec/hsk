# -*- coding: utf-8 -*-
"""Главное меню — iOS Liquid Glass с иерархией и sidebar-виджетами."""
import math

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.glass import (liquid_card_qss, icon_tile_qss, sidebar_qss,
                      continue_card_qss, streak_card_qss,
                      soft_shadow)
from core.i18n import i18n
from core.config import APP_NAME, APP_VERSION
from core.storage import storage


# (ключ_i18n, action_id, иконка, subtitle_ключ, цвет плитки)
MENU_ITEMS = [
    ("menu_lessons", "lessons", "lessons",
     {"ru": "18 уроков · 727 слов", "tk": "18 sapak · 727 söz", "en": "18 lessons · 727 words"},
     ("rgba(74, 158, 255, 60)", "rgba(120, 180, 255, 100)")),
    ("menu_vocab", "vocab", "vocab",
     {"ru": "Поиск по всем урокам", "tk": "Ähli sapaklarda gözleg", "en": "Search all lessons"},
     ("rgba(245, 184, 73, 60)", "rgba(255, 210, 120, 100)")),
    ("menu_srs", "srs", "srs",
     {"ru": "SM-2 spaced repetition", "tk": "SM-2 aralykly gaýtalama", "en": "SM-2 spaced repetition"},
     ("rgba(77, 212, 200, 60)", "rgba(130, 230, 220, 100)")),
    ("menu_heatmap", "heatmap", "heatmap",
     {"ru": "365-дневная карта", "tk": "365 günlük karta", "en": "365-day activity map"},
     ("rgba(155, 126, 232, 60)", "rgba(190, 165, 255, 100)")),
    ("menu_stats", "stats", "stats",
     {"ru": "Статистика и графики", "tk": "Statistika we grafikler", "en": "Statistics and charts"},
     ("rgba(92, 214, 142, 60)", "rgba(140, 235, 180, 100)")),
    ("analyzer_title", "analyzer", "analyzer",
     {"ru": "Разбор иероглифов", "tk": "Iýeroglifleriň derňewi", "en": "Character analysis"},
     ("rgba(240, 108, 154, 60)", "rgba(255, 150, 190, 100)")),
    ("menu_grammar_lib", "grammar_lib", "grammar",
     {"ru": "Все правила", "tk": "Ähli düzgünler", "en": "All grammar"},
     ("rgba(155, 126, 232, 60)", "rgba(190, 165, 255, 100)")),
    ("menu_compare_lib", "compare_lib", "analyzer",
     {"ru": "Различия слов", "tk": "Söz tapawutlary", "en": "Word differences"},
     ("rgba(77, 212, 200, 60)", "rgba(130, 230, 220, 100)")),
]


def strip_icon(s: str) -> str:
    s = s.strip()
    if s and ord(s[0]) > 0x2000:
        idx = s.find(" ")
        if idx > 0:
            return s[idx + 1:]
    return s


# ============================================================
class GlassCard(QFrame):
    """Стеклянная карточка: [иконка] [заголовок + подзаголовок] [›]"""
    clicked = pyqtSignal()
    hover_changed = pyqtSignal(bool)

    def __init__(self, title, subtitle, icon_name, colors, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(int(64 * qt_theme.scale))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(liquid_card_qss())

        s = qt_theme.scale
        color_rgba, border_rgba = colors

        lay = QHBoxLayout(self)
        lay.setContentsMargins(int(18 * s), int(8 * s),
                               int(18 * s), int(8 * s))
        lay.setSpacing(0)

        # --- Иконка-плитка 48×48 ---
        tile = QFrame()
        tile.setObjectName("iconTile")
        tile.setFixedSize(int(40 * s), int(40 * s))
        tile.setStyleSheet(icon_tile_qss(color_rgba, border_rgba,
                                          radius=int(12 * s)))
        tl = QVBoxLayout(tile)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setAlignment(Qt.AlignCenter)

        self.icon_lbl = QLabel(icon(icon_name))
        self._base_icon_size = int(22 * s)
        self.icon_lbl.setFont(get_icon_font(self._base_icon_size))
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        self.icon_lbl.setStyleSheet("background: transparent; color: #FFFFFF;")
        tl.addWidget(self.icon_lbl)
        lay.addWidget(tile)
        lay.addSpacing(int(14 * s))

        # --- Текстовый блок: заголовок + подзаголовок ---
        text_box = QVBoxLayout()
        text_box.setContentsMargins(0, 0, 0, 0)
        text_box.setSpacing(int(1 * s))

        title_lbl = QLabel(title)
        f = qt_theme.font("card")
        f.setPointSize(int(14 * qt_theme.scale))
        title_lbl.setFont(f)
        title_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        text_box.addWidget(title_lbl)

        # Подзаголовок — язык выбирается динамически
        sub = subtitle.get(i18n.language, subtitle.get("en", ""))
        self.subtitle_lbl = QLabel(sub)
        f2 = qt_theme.font("muted")
        f2.setPointSize(int(9 * qt_theme.scale))
        self.subtitle_lbl.setFont(f2)
        self.subtitle_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        text_box.addWidget(self.subtitle_lbl)

        lay.addLayout(text_box)
        lay.addStretch()

        # --- Chevron ---
        self.chevron = QLabel(icon("chevron"))
        self.chevron.setFont(get_icon_font(int(20 * s)))
        self.chevron.setFixedWidth(int(24 * s))
        self.chevron.setAlignment(Qt.AlignCenter)
        self.chevron.setStyleSheet(
            f"color: rgba(140, 180, 220, 130); background: transparent;")
        lay.addWidget(self.chevron)

        # Анимация
        self._hovered = False
        self._phase = 0.0
        self._current_factor = 1.0


    def enterEvent(self, event):
        self._hovered = True
        self.hover_changed.emit(True)
        self.chevron.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.hover_changed.emit(False)
        self.chevron.setStyleSheet(
            "color: rgba(140, 180, 220, 130); background: transparent;")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def is_animating(self):
        if self._hovered:
            return True
        return abs(self._current_factor - 1.0) > 0.005

    def animate(self):
        if self._hovered:
            self._phase += 0.22
            target = 1.0 + 0.15 * math.sin(self._phase)
        else:
            target = 1.0
        self._current_factor += (target - self._current_factor) * 0.30
        size = max(8, int(self._base_icon_size * self._current_factor))
        self.icon_lbl.setFont(get_icon_font(size))


# ============================================================
class MainMenuScreen(QWidget):
    open_screen = pyqtSignal(str)
    toggle_theme = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self._cards = []
        self._timer = QTimer(self)
        self._timer.setInterval(30)
        self._timer.timeout.connect(self._tick)
        self._build()

    # ------------------------------------------------------------
    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(48 * s), int(24 * s),
                                int(48 * s), int(20 * s))
        root.setSpacing(0)

        # ============== Заголовок ==============
        header = QHBoxLayout()
        header.setSpacing(int(14 * s))

        logo = QLabel("\u4e2d\u6587")
        logo.setFont(qt_theme.font("logo"))
        logo.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        header.addWidget(logo)

        dot = QLabel("\u00b7")
        dot.setFont(qt_theme.font("h1"))
        dot.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        header.addWidget(dot)

        title = QLabel(APP_NAME)
        title.setFont(qt_theme.font("h1"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        header.addWidget(title)
        header.addStretch()
        root.addLayout(header)

        version = QLabel(f"v{APP_VERSION}")
        version.setFont(qt_theme.font("muted"))
        version.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        root.addWidget(version)
        root.addSpacing(int(20 * s))

        # ============== Основная зона ==============
        cols = QHBoxLayout()
        cols.setSpacing(int(24 * s))

        # Левая колонка: карточки
        left = QVBoxLayout()
        left.setSpacing(int(14 * s))

        for key, action, icon_name, subtitle, colors in MENU_ITEMS:
            title_text = strip_icon(i18n.t(key))
            card = GlassCard(title_text, subtitle, icon_name, colors, parent=self)
            card.clicked.connect(
                lambda _c=False, a=action: self.open_screen.emit(a))
            card.hover_changed.connect(self._on_hover)
            self._cards.append(card)
            left.addWidget(card)

        left.addStretch()
        cols.addLayout(left, 1)

        # Правая колонка: sidebar
        sidebar = self._make_sidebar()
        cols.addWidget(sidebar, 0)

        root.addLayout(cols, 1)

    # ------------------------------------------------------------
    def _make_sidebar(self):
        s = qt_theme.scale
        panel = QFrame()
        panel.setObjectName("sidebar")
        panel.setFixedWidth(int(310 * s))
        panel.setStyleSheet(sidebar_qss())

        lay = QVBoxLayout(panel)
        lay.setContentsMargins(int(16 * s), int(18 * s),
                               int(16 * s), int(18 * s))
        lay.setSpacing(int(12 * s))

        # ============ 1. Продолжить последний урок ============
        self._make_continue_card(lay)
        lay.addSpacing(int(4 * s))

        # ============ 2. Мини-настройки ============

        # ============ 3. Растяжка ============
        lay.addSpacing(int(8 * s))

        # ============ 4. Streak-виджет ============
        self._make_streak_card(lay)

        # ============ 5. Прогресс HSK 5 ============
        self._make_progress_card(lay)

        b_settings = self._side_button("menu_settings", "settings")
        b_settings.clicked.connect(lambda: self.open_screen.emit("settings"))
        lay.addWidget(b_settings)

        lay.addStretch()
        return panel

    # ------------------------------------------------------------
    def _make_continue_card(self, parent_layout):
        """Карточка «Продолжить последний урок»."""
        s = qt_theme.scale
        card = QFrame()
        card.setObjectName("continueCard")
        card.setStyleSheet(continue_card_qss())
        card.setCursor(Qt.PointingHandCursor)
        card.setMinimumHeight(int(72 * s))

        lay = QHBoxLayout(card)
        lay.setContentsMargins(int(16 * s), int(12 * s),
                               int(16 * s), int(12 * s))
        lay.setSpacing(int(12 * s))

        ic = QLabel(icon("play"))
        ic.setFont(get_icon_font(int(24 * s)))
        ic.setStyleSheet("background: transparent; color: #FFFFFF;")
        lay.addWidget(ic)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)

        title = QLabel({
            "ru": "Продолжить",
            "tk": "Dowam et",
            "en": "Continue",
        }.get(i18n.language, "Continue"))
        f = qt_theme.font("body_bold")
        title.setFont(f)
        title.setStyleSheet("background: transparent; color: #FFFFFF;")
        text_box.addWidget(title)

        last = storage.get("last_lesson") or "unit1_lesson1"
        try:
            unit = int(last.split("unit")[1].split("_")[0])
            lesson = int(last.split("_lesson")[1])
            label = f"Урок {unit}.{lesson}"
        except Exception:
            label = "Урок 1.1"

        sub = QLabel(label)
        f2 = qt_theme.font("muted")
        sub.setFont(f2)
        sub.setStyleSheet("background: transparent; color: rgba(255,255,255,200);")
        text_box.addWidget(sub)

        lay.addLayout(text_box)
        lay.addStretch()

        card.mousePressEvent = lambda _e: self.open_screen.emit("lessons")
        parent_layout.addWidget(card)

    # ------------------------------------------------------------
    def _make_streak_card(self, parent_layout):
        """Виджет со streak (дни подряд)."""
        s = qt_theme.scale
        streak = storage.get("streak_days", 0)

        card = QFrame()
        card.setObjectName("streakCard")
        card.setStyleSheet(streak_card_qss())
        card.setMinimumHeight(int(72 * s))

        lay = QHBoxLayout(card)
        lay.setContentsMargins(int(16 * s), int(12 * s),
                               int(16 * s), int(12 * s))
        lay.setSpacing(int(14 * s))

        ic = QLabel(icon("streak"))
        ic.setFont(get_icon_font(int(32 * s)))
        ic.setStyleSheet("background: transparent; color: #FFFFFF;")
        lay.addWidget(ic)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)

        num = QLabel(str(streak))
        f = qt_theme.font("h2")
        num.setFont(f)
        num.setStyleSheet("background: transparent; color: #FFFFFF;")
        text_box.addWidget(num)

        label = QLabel({
            "ru": "дней подряд",
            "tk": "gün yzygiderli",
            "en": "days in a row",
        }.get(i18n.language, "days in a row"))
        f2 = qt_theme.font("muted")
        label.setFont(f2)
        label.setStyleSheet("background: transparent; color: rgba(255,255,255,200);")
        text_box.addWidget(label)

        lay.addLayout(text_box)
        lay.addStretch()
        parent_layout.addWidget(card)

    # ------------------------------------------------------------
    def _make_progress_card(self, parent_layout):
        """Прогресс по HSK 5 上 (18 уроков)."""
        s = qt_theme.scale
        completed = storage.get("completed_lessons", [])
        total_lessons = 18
        done = len(completed)
        percent = int(round(100 * done / total_lessons)) if total_lessons else 0

        wrap = QVBoxLayout()
        wrap.setSpacing(int(6 * s))

        label_row = QHBoxLayout()
        lbl = QLabel({
            "ru": "Прогресс курса",
            "tk": "Kursyň ösüşi",
            "en": "Course progress",
        }.get(i18n.language, "Course progress"))
        f = qt_theme.font("muted")
        lbl.setFont(f)
        lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        label_row.addWidget(lbl)
        label_row.addStretch()

        val = QLabel(f"{done}/{total_lessons}")
        f2 = qt_theme.font("body_bold")
        val.setFont(f2)
        val.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        label_row.addWidget(val)

        wrap.addLayout(label_row)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(percent)
        bar.setTextVisible(False)
        bar.setFixedHeight(int(8 * s))
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: rgba(80, 120, 160, 60);
                border: none;
                border-radius: {int(4 * s)}px;
            }}
            QProgressBar::chunk {{
                background-color: {qt_theme.c('accent')};
                border-radius: {int(4 * s)}px;
            }}
        """)
        wrap.addWidget(bar)

        parent_layout.addLayout(wrap)

    # ------------------------------------------------------------
    def _side_button(self, key, icon_name):
        s = qt_theme.scale
        btn = QPushButton()
        btn.setObjectName("sideBtn")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(int(48 * s))
        text = strip_icon(i18n.t(key))
        btn.setText(f"  {icon(icon_name)}     {text}")
        # Иконочный шрифт для символа, текстовый — для остального.
        # Qt не умеет смешивать шрифты в одном виджете — используем
        # технику: устанавливаем UI-шрифт, символы всё равно отрисуются.
        btn.setFont(get_icon_font(int(14 * s)))

        # Специальная обработка кликов
        if key == "change_lang":
            btn.clicked.connect(self.change_lang.emit)
        elif key in ("theme_light", "theme_dark"):
            btn.clicked.connect(self.toggle_theme.emit)
        return btn

    # ------------------------------------------------------------
    def _on_hover(self, is_hover):
        if is_hover:
            if not self._timer.isActive():
                self._timer.start()

    def _tick(self):
        any_active = False
        for card in self._cards:
            if card.is_animating():
                card.animate()
                any_active = True
        if not any_active:
            self._timer.stop()
