# -*- coding: utf-8 -*-
"""Экран выбора языка — стеклянные карточки."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.glass import (liquid_card_qss, icon_tile_qss, soft_shadow)
from core.i18n import i18n
from core.config import APP_NAME, APP_VERSION
from core.storage import storage


LANGUAGES = [
    ("ru", "Русский",   "🇷🇺", "Russian"),
    ("tk", "Türkmençe", "🇹🇲", "Turkmen"),
    ("en", "English",   "🇬🇧", "English"),
    ("uz", "O'zbekcha", "🇺🇿", "Uzbek"),
    ("tg", "Тоҷикӣ",    "🇹🇯", "Tajik"),
]


class LanguageCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, code, name, flag, parent=None):
        super().__init__(parent)
        self.code = code
        self.setObjectName("glassCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(int(88 * qt_theme.scale))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(liquid_card_qss())

        s = qt_theme.scale

        lay = QHBoxLayout(self)
        lay.setContentsMargins(int(20 * s), int(14 * s),
                               int(24 * s), int(14 * s))
        lay.setSpacing(int(18 * s))

        # Флаг-плитка
        tile = QFrame()
        tile.setObjectName("iconTile")
        tile.setFixedSize(int(56 * s), int(56 * s))
        tile.setStyleSheet(icon_tile_qss("rgba(120, 170, 220, 40)",
                                          "rgba(180, 210, 240, 80)",
                                          radius=int(14 * s)))
        tl = QVBoxLayout(tile)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setAlignment(Qt.AlignCenter)

        flag_lbl = QLabel(flag)
        flag_lbl.setFont(get_icon_font(int(30 * s)))
        flag_lbl.setAlignment(Qt.AlignCenter)
        flag_lbl.setStyleSheet("background: transparent;")
        tl.addWidget(flag_lbl)
        lay.addWidget(tile)

        # Имя языка
        name_lbl = QLabel(name)
        f = qt_theme.font("card")
        f.setPointSize(int(17 * qt_theme.scale))
        name_lbl.setFont(f)
        name_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        lay.addWidget(name_lbl)
        lay.addStretch()

        # Chevron
        self.chevron = QLabel(icon("chevron"))
        self.chevron.setFont(get_icon_font(int(20 * s)))
        self.chevron.setFixedWidth(int(24 * s))
        self.chevron.setAlignment(Qt.AlignCenter)
        self.chevron.setStyleSheet(
            "color: rgba(140, 180, 220, 130); background: transparent;")
        lay.addWidget(self.chevron)


    def enterEvent(self, event):
        self.chevron.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.chevron.setStyleSheet(
            "color: rgba(140, 180, 220, 130); background: transparent;")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.code)
        super().mousePressEvent(event)


class LanguageSelectScreen(QWidget):
    language_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(48 * s), int(36 * s),
                                int(48 * s), int(36 * s))
        root.setSpacing(0)

        # Заголовок
        header = QHBoxLayout()
        header.setSpacing(int(14 * s))

        logo = QLabel("中文")
        logo.setFont(qt_theme.font("logo"))
        logo.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        header.addWidget(logo)

        dot = QLabel("·")
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
        root.addSpacing(int(50 * s))

        # Подзаголовок по центру
        title_row = QVBoxLayout()
        title_row.setSpacing(int(6 * s))

        big = QLabel(i18n.t("lang_title"))
        big.setFont(qt_theme.font("h2"))
        big.setAlignment(Qt.AlignCenter)
        big.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        title_row.addWidget(big)

        sub = QLabel(i18n.t("lang_sub"))
        f = qt_theme.font("muted")
        sub.setFont(f)
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        title_row.addWidget(sub)

        root.addLayout(title_row)
        root.addSpacing(int(36 * s))

        # Карточки языков по центру
        cards_wrap = QHBoxLayout()
        cards_wrap.addStretch()

        cards_col = QVBoxLayout()
        cards_col.setSpacing(int(14 * s))

        for code, name, flag, _ in LANGUAGES:
            card = LanguageCard(code, name, flag, parent=self)
            card.setFixedWidth(int(520 * s))
            card.clicked.connect(self._on_pick)
            cards_col.addWidget(card)

        cards_wrap.addLayout(cards_col)
        cards_wrap.addStretch()

        root.addLayout(cards_wrap)
        root.addStretch()

    def _on_pick(self, code):
        storage.set("language", code)
        i18n.set_language(code)
        self.language_selected.emit(code)
