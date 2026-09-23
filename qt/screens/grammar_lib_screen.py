# -*- coding: utf-8 -*-
"""Библиотека грамматики — все правила из всех уроков."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QLineEdit, QComboBox, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QFont

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.glass import opaque_card_qss, opaque_icon_tile_qss
from qt.widgets import (OpaqueScrollPage, BackButton, scroll_bg_color)
from core.i18n import i18n
from models.lesson import load_lesson


UNIT_COLORS = {
    1: ("#3A6088", "#5A80A8"),
    2: ("#3A7060", "#5A9080"),
    3: ("#7A6030", "#9A8050"),
    4: ("#5A4A88", "#7A6AA8"),
    5: ("#3A7080", "#5A90A0"),
    6: ("#7A3A60", "#9A5A80"),
}


class GrammarCard(QFrame):
    def __init__(self, gp, unit, lesson_idx, parent=None):
        super().__init__(parent)
        s = qt_theme.scale
        self.setObjectName("glassCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setStyleSheet(opaque_card_qss())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(int(22 * s), int(16 * s),
                               int(22 * s), int(16 * s))
        lay.setSpacing(int(10 * s))

        # Заголовок: word + pos + badge урока
        head = QHBoxLayout()
        head.setSpacing(int(10 * s))

        word = QLabel(gp.word)
        f = QFont(qt_theme._cjk)
        f.setPointSize(int(22 * s))
        f.setBold(True)
        word.setFont(f)
        word.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        head.addWidget(word)

        if gp.pos:
            pos = QLabel(gp.pos)
            pos.setFont(qt_theme.font("muted"))
            pos.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            head.addWidget(pos)

        head.addStretch()

        # Бейдж урока
        badge = QFrame()
        badge.setFixedHeight(int(26 * s))
        color, border = UNIT_COLORS.get(unit, UNIT_COLORS[1])
        badge.setStyleSheet(
            f"QFrame {{ background-color: {color}; "
            f"border: 1px solid {border}; border-radius: {int(13 * s)}px; }}"
        )
        bl = QHBoxLayout(badge)
        bl.setContentsMargins(int(12 * s), 0, int(12 * s), 0)
        badge_lbl = QLabel(f"Урок {unit}.{lesson_idx}")
        badge_lbl.setFont(qt_theme.font("muted"))
        badge_lbl.setStyleSheet(
            "background: transparent; color: #FFFFFF; font-weight: bold;")
        bl.addWidget(badge_lbl)
        head.addWidget(badge)
        lay.addLayout(head)

        # Объяснение
        expl = QLabel(gp.explanation.get(i18n.language, ""))
        expl.setWordWrap(True)
        expl.setFont(qt_theme.font("body"))
        expl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        expl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lay.addWidget(expl)

        # Примеры (первые 3)
        for i, ex in enumerate(gp.examples[:3], 1):
            ex_card = QFrame()
            ex_card.setStyleSheet(
                "QFrame { background-color: rgba(28, 44, 62, 180); "
                "border: 1px solid rgba(120, 160, 200, 60); "
                f"border-radius: {int(10 * s)}px; }}"
            )
            el = QVBoxLayout(ex_card)
            el.setContentsMargins(int(14 * s), int(10 * s),
                                  int(14 * s), int(10 * s))
            el.setSpacing(int(4 * s))

            zh = QLabel(f"{i}. {ex.get('zh', '')}")
            fz = QFont(qt_theme._cjk)
            fz.setPointSize(int(12 * s))
            zh.setFont(fz)
            zh.setWordWrap(True)
            zh.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            zh.setTextInteractionFlags(Qt.TextSelectableByMouse)
            el.addWidget(zh)

            tr = ex.get(i18n.language, "")
            if tr:
                tl = QLabel(tr)
                tl.setWordWrap(True)
                tl.setFont(qt_theme.font("muted"))
                tl.setStyleSheet(
                    f"color: {qt_theme.c('text_muted')}; background: transparent;")
                tl.setTextInteractionFlags(Qt.TextSelectableByMouse)
                el.addWidget(tl)

            lay.addWidget(ex_card)


class GrammarLibScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)

        # Собираем грамматики со всех уроков
        self.all_grammars = []  # list of (unit, lesson_idx, gp)
        for unit in range(1, 7):
            for idx in range(1, 4):
                try:
                    lesson = load_lesson(unit, idx)
                except Exception:
                    continue
                for gp in lesson.grammar:
                    self.all_grammars.append((unit, idx, gp))

        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        # Верх
        top = QHBoxLayout()
        top.setSpacing(int(14 * s))
        back = BackButton(i18n.t("back_btn"))
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        title = QLabel(i18n.t("grammar_lib_title"))
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        title_box.addWidget(title)

        self.sub_lbl = QLabel(f"{len(self.all_grammars)} грамматик")
        self.sub_lbl.setFont(qt_theme.font("muted"))
        self.sub_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        title_box.addWidget(self.sub_lbl)

        top.addLayout(title_box)
        top.addStretch()
        root.addLayout(top)

        # Панель управления
        ctrl = QHBoxLayout()
        ctrl.setSpacing(int(10 * s))

        self.search = QLineEdit()
        self.search.setPlaceholderText(i18n.t("grammar_search_ph"))
        self.search.setMinimumHeight(int(40 * s))
        self.search.setFont(QFont(qt_theme._cjk, int(12 * s)))
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(30, 46, 62, 220);
                border: 1px solid rgba(120, 160, 200, 80);
                border-radius: 10px;
                padding: 6px 14px;
                color: {qt_theme.c('text')};
            }}
            QLineEdit:focus {{ border: 1px solid {qt_theme.c('accent')}; }}
        """)
        self.search.textChanged.connect(self._refresh)
        ctrl.addWidget(self.search, 1)

        self.filter = QComboBox()
        self.filter.setMinimumHeight(int(40 * s))
        self.filter.setMinimumWidth(int(160 * s))
        self.filter.setFont(QFont(qt_theme._ui, int(12 * s)))
        self.filter.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(30, 46, 62, 220);
                border: 1px solid rgba(120, 160, 200, 80);
                border-radius: 10px;
                padding: 6px 14px;
                color: {qt_theme.c('text')};
            }}
            QComboBox::drop-down {{ border: none; width: 28px; }}
            QComboBox QAbstractItemView {{
                background-color: rgba(20, 34, 48, 250);
                border: 1px solid rgba(120, 160, 200, 80);
                color: {qt_theme.c('text')};
                selection-background-color: rgba(74, 158, 255, 120);
            }}
        """)
        self.filter.addItem(i18n.t("grammar_all"), None)
        for u in range(1, 7):
            self.filter.addItem(f"Юнит {u}", u)
        self.filter.currentIndexChanged.connect(self._refresh)
        ctrl.addWidget(self.filter)

        root.addLayout(ctrl)

        # Скролл
        self.scroll = OpaqueScrollPage()
        root.addWidget(self.scroll, 1)

        self._refresh()

    def _refresh(self):
        # Очищаем
        while self.scroll.lay.count():
            item = self.scroll.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        query = self.search.text().strip().lower()
        unit_filter = self.filter.currentData()

        count = 0
        for unit, idx, gp in self.all_grammars:
            if unit_filter and unit != unit_filter:
                continue
            if query:
                haystack = " ".join([
                    gp.word, gp.pos,
                    gp.explanation.get("ru", ""),
                    gp.explanation.get("tk", ""),
                    gp.explanation.get("en", ""),
                ]).lower()
                if query not in haystack:
                    continue
            self.scroll.lay.addWidget(GrammarCard(gp, unit, idx, parent=self))
            count += 1

        self.scroll.lay.addStretch()
        self.sub_lbl.setText(
            f"{i18n.t('grammar_found')}: {count} / {len(self.all_grammars)}"
        )
