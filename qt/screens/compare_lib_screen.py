# -*- coding: utf-8 -*-
"""Библиотека сравнений слов."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QLineEdit, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QFont

from qt.theme import qt_theme
from qt.icons import get_icon_font
from qt.glass import opaque_card_qss
from qt.widgets import OpaqueScrollPage, BackButton, scroll_bg_color
from core.i18n import i18n
from models.lesson import load_lesson


class CompareCard(QFrame):
    def __init__(self, cp, unit, lesson_idx, parent=None):
        super().__init__(parent)
        s = qt_theme.scale
        self.setObjectName("glassCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setStyleSheet(opaque_card_qss())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(int(22 * s), int(18 * s),
                               int(22 * s), int(18 * s))
        lay.setSpacing(int(12 * s))

        # Заголовок: A vs B + бейдж урока
        head = QHBoxLayout()
        head.setSpacing(int(14 * s))

        a_lbl = QLabel(cp.word_a)
        f_a = QFont(qt_theme._cjk)
        f_a.setPointSize(int(20 * s))
        f_a.setBold(True)
        a_lbl.setFont(f_a)
        a_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        head.addWidget(a_lbl)

        vs = QLabel(i18n.t("compare_vs"))
        vs.setFont(qt_theme.font("muted"))
        vs.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        head.addWidget(vs)

        b_lbl = QLabel(cp.word_b)
        b_lbl.setFont(f_a)
        b_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent_dark') if hasattr(qt_theme.c, '__call__') else qt_theme.c('accent')}; "
            f"background: transparent;")
        b_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        head.addWidget(b_lbl)
        head.addStretch()

        badge = QLabel(f"Урок {unit}.{lesson_idx}")
        badge.setFont(qt_theme.font("muted"))
        badge.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; "
            f"background-color: rgba(60, 80, 100, 150); "
            f"border-radius: 10px; padding: 4px 12px;")
        head.addWidget(badge)
        lay.addLayout(head)

        # Общее
        common_lbl = QLabel("≈  " + i18n.t("compare_common"))
        common_lbl.setFont(qt_theme.font("muted"))
        common_lbl.setStyleSheet(
            f"color: {qt_theme.c('success')}; background: transparent; "
            f"font-weight: bold;")
        lay.addWidget(common_lbl)

        common_txt = QLabel(cp.common.get(i18n.language, ""))
        common_txt.setWordWrap(True)
        common_txt.setFont(qt_theme.font("body"))
        common_txt.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        common_txt.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lay.addWidget(common_txt)

        # Различия
        diff_lbl = QLabel("≠  " + i18n.t("compare_diff"))
        diff_lbl.setFont(qt_theme.font("muted"))
        diff_lbl.setStyleSheet(
            f"color: {qt_theme.c('error')}; background: transparent; "
            f"font-weight: bold;")
        lay.addWidget(diff_lbl)

        for d in cp.differences:
            dl = QLabel("•  " + d.get(i18n.language, ""))
            dl.setWordWrap(True)
            dl.setFont(qt_theme.font("body"))
            dl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            dl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            lay.addWidget(dl)


class CompareLibScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)

        # Собираем сравнения
        self.all_comparisons = []
        for unit in range(1, 7):
            for idx in range(1, 4):
                try:
                    lesson = load_lesson(unit, idx)
                except Exception:
                    continue
                for cp in lesson.comparisons:
                    self.all_comparisons.append((unit, idx, cp))

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

        title = QLabel(i18n.t("compare_lib_title"))
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        title_box.addWidget(title)

        self.sub_lbl = QLabel(f"{len(self.all_comparisons)} сравнений")
        self.sub_lbl.setFont(qt_theme.font("muted"))
        self.sub_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        title_box.addWidget(self.sub_lbl)

        top.addLayout(title_box)
        top.addStretch()
        root.addLayout(top)

        # Поиск
        self.search = QLineEdit()
        self.search.setPlaceholderText(i18n.t("compare_search_ph"))
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
        root.addWidget(self.search)

        # Скролл
        self.scroll = OpaqueScrollPage()
        root.addWidget(self.scroll, 1)

        self._refresh()

    def _refresh(self):
        while self.scroll.lay.count():
            item = self.scroll.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        q = self.search.text().strip().lower()
        count = 0
        for unit, idx, cp in self.all_comparisons:
            if q:
                haystack = " ".join([
                    cp.word_a, cp.word_b,
                    cp.common.get("ru", ""),
                    cp.common.get("tk", ""),
                    cp.common.get("en", ""),
                    " ".join(d.get("ru", "") for d in cp.differences),
                    " ".join(d.get("tk", "") for d in cp.differences),
                    " ".join(d.get("en", "") for d in cp.differences),
                ]).lower()
                if q not in haystack:
                    continue
            self.scroll.lay.addWidget(CompareCard(cp, unit, idx, parent=self))
            count += 1

        self.scroll.lay.addStretch()
        self.sub_lbl.setText(
            f"Найдено: {count} / {len(self.all_comparisons)}"
        )
