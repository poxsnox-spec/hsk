# -*- coding: utf-8 -*-
"""Анализатор иероглифов."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from qt.theme import qt_theme
from qt.widgets import ScrollPage, GlassCard, InnerCard, PageHeader
from core.i18n import i18n
from models.lesson import load_lesson
from data.hanzi_db import analyze, split_pinyin, TONE_NAMES


class AnalyzerScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, unit=1, index=1, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.unit = unit
        self.index = index
        try:
            self.lesson = load_lesson(unit, index)
        except Exception:
            self.lesson = None
        self.selected = None
        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        header = PageHeader(i18n.t("analyzer_title"))
        header.back_clicked.connect(self.back_requested.emit)
        root.addWidget(header)

        # Выпадающий список слов
        if self.lesson:
            picker = QHBoxLayout()
            picker.setSpacing(int(10 * s))

            lbl = QLabel(i18n.t("analyzer_word"))
            lbl.setFont(qt_theme.font("body"))
            lbl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            picker.addWidget(lbl)

            self.combo = QComboBox()
            self.combo.setMinimumHeight(int(40 * s))
            self.combo.setFont(QFont(qt_theme._cjk, int(13 * s)))
            self.combo.setStyleSheet(f"""
                QComboBox {{
                    background-color: rgba(40, 60, 84, 180);
                    border: 1px solid rgba(120, 160, 200, 70);
                    border-radius: 10px;
                    padding: 6px 12px;
                    color: {qt_theme.c('text')};
                }}
                QComboBox:hover {{
                    background-color: rgba(60, 90, 120, 200);
                    border: 1px solid {qt_theme.c('accent')};
                }}
                QComboBox::drop-down {{ border: none; width: 24px; }}
                QComboBox QAbstractItemView {{
                    background-color: rgba(30, 45, 62, 240);
                    border: 1px solid rgba(120, 160, 200, 70);
                    color: {qt_theme.c('text')};
                    selection-background-color: rgba(74, 158, 255, 120);
                }}
            """)
            for w in self.lesson.vocabulary:
                self.combo.addItem(w.hanzi)
            self.combo.currentIndexChanged.connect(self._on_pick)

            picker.addWidget(self.combo, 1)
            picker_w = QWidget()
            picker_w.setLayout(picker)
            root.addWidget(picker_w)

        self._content = ScrollPage(self)
        root.addWidget(self._content, 1)

        if self.lesson and self.lesson.vocabulary:
            self.selected = self.lesson.vocabulary[0]
            self._render()

    def _on_pick(self, idx):
        if self.lesson and 0 <= idx < len(self.lesson.vocabulary):
            self.selected = self.lesson.vocabulary[idx]
            self._render()

    def _clear(self):
        while self._content.lay.count():
            item = self._content.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _render(self):
        self._clear()
        s = qt_theme.scale
        w = self.selected

        # Карточка слова
        card = GlassCard()
        cl = QHBoxLayout(card)
        cl.setContentsMargins(int(24 * s), int(20 * s),
                              int(24 * s), int(20 * s))
        cl.setSpacing(int(24 * s))

        hz = QLabel(w.hanzi)
        fh = QFont(qt_theme._cjk)
        fh.setPointSize(int(48 * s))
        fh.setBold(True)
        hz.setFont(fh)
        hz.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(hz)

        info = QVBoxLayout()
        info.setSpacing(4)

        py = QLabel(w.pinyin)
        fp = QFont("Arial", int(16 * s))
        py.setFont(fp)
        py.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        info.addWidget(py)

        tr = QLabel(f"({w.pos})  {w.translate(i18n.language)}")
        tr.setFont(qt_theme.font("body"))
        tr.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        info.addWidget(tr)

        cl.addLayout(info)
        cl.addStretch()
        self._content.lay.addWidget(card)

        # Разбор пиньиня
        self._render_pinyin(w)

        # Иероглифы
        for ch in w.hanzi:
            self._render_char(ch)

        self._content.lay.addStretch()

    def _render_pinyin(self, w):
        s = qt_theme.scale
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(22 * s), int(16 * s),
                              int(22 * s), int(16 * s))
        cl.setSpacing(int(10 * s))

        title = QLabel(i18n.t("analyzer_pinyin_split"))
        ft = qt_theme.font("h3")
        title.setFont(ft)
        title.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(int(8 * s))
        for syl in split_pinyin(w.pinyin):
            box = InnerCard()
            bl = QVBoxLayout(box)
            bl.setContentsMargins(int(12 * s), int(8 * s),
                                  int(12 * s), int(8 * s))
            bl.setSpacing(2)

            d = QLabel(syl["display"])
            fd = QFont("Arial", int(18 * s))
            fd.setBold(True)
            d.setFont(fd)
            d.setAlignment(Qt.AlignCenter)
            d.setStyleSheet(
                f"color: {qt_theme.c('accent')}; background: transparent;")
            bl.addWidget(d)

            t = QLabel(f"тон {syl['tone']}")
            t.setFont(qt_theme.font("muted"))
            t.setAlignment(Qt.AlignCenter)
            t.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            bl.addWidget(t)

            row.addWidget(box)

        row.addStretch()
        wrap = QWidget()
        wrap.setLayout(row)
        cl.addWidget(wrap)
        self._content.lay.addWidget(card)

    def _render_char(self, ch):
        meta = analyze(ch)
        if not meta:
            return
        s = qt_theme.scale
        card = GlassCard()
        cl = QHBoxLayout(card)
        cl.setContentsMargins(int(22 * s), int(16 * s),
                              int(22 * s), int(16 * s))
        cl.setSpacing(int(20 * s))

        hz = QLabel(ch)
        fh = QFont(qt_theme._cjk)
        fh.setPointSize(int(36 * s))
        fh.setBold(True)
        hz.setFont(fh)
        hz.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        cl.addWidget(hz)

        info = QVBoxLayout()
        info.setSpacing(4)

        for k, v in (("Радикал:", f"{meta['radical']} ({meta.get('radical_ru','')})"),
                     ("Черт:", str(meta["strokes"])),
                     ("Компоненты:", " + ".join(meta["components"]))):
            row = QHBoxLayout()
            kl = QLabel(k)
            kl.setFont(qt_theme.font("muted"))
            kl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            kl.setFixedWidth(int(140 * s))
            row.addWidget(kl)
            vl = QLabel(v)
            fv = QFont(qt_theme._cjk)
            fv.setPointSize(int(12 * s))
            vl.setFont(fv)
            vl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            row.addWidget(vl)
            row.addStretch()
            w_row = QWidget()
            w_row.setLayout(row)
            info.addWidget(w_row)

        cl.addLayout(info)
        cl.addStretch()
        self._content.lay.addWidget(card)
