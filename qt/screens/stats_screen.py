# -*- coding: utf-8 -*-
"""Экран прогресса — сводка и результаты."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from qt.theme import qt_theme
from qt.widgets import ScrollPage, GlassCard, InnerCard, PageHeader
from core.i18n import i18n
from core.storage import storage
from models.lesson import load_lesson


class StatsScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        header = PageHeader(i18n.t("menu_stats"))
        header.back_clicked.connect(self.back_requested.emit)
        root.addWidget(header)

        content = ScrollPage(self)
        root.addWidget(content, 1)

        # Данные
        scores = storage.get("lesson_scores", {}) or {}
        completed = storage.get("completed_lessons", []) or []
        vocab_stats = storage.get("vocab_stats", {}) or {}

        # Сводка
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(22 * s), int(18 * s),
                              int(22 * s), int(18 * s))
        cl.setSpacing(int(10 * s))

        title = QLabel(i18n.t("stats_summary"))
        ft = qt_theme.font("h3")
        title.setFont(ft)
        title.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(title)

        total_words = len(vocab_stats)
        correct = sum(s.get("correct", 0) for s in vocab_stats.values())
        seen = sum(s.get("seen", 0) for s in vocab_stats.values())
        avg = round(100 * correct / seen) if seen else 0
        total_attempts = sum(s.get("attempts", 0) for s in scores.values())

        rows = [
            ("📚 Слов изучено",  str(total_words)),
            ("🎯 Средний балл",  f"{avg}%"),
            ("🏆 Попыток",        str(total_attempts)),
            ("✅ Уроков",          f"{len(completed)} / 18"),
        ]
        for k, v in rows:
            r = QHBoxLayout()
            kl = QLabel(k)
            kl.setFont(qt_theme.font("body"))
            kl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            r.addWidget(kl)
            r.addStretch()
            vl = QLabel(v)
            vl.setFont(qt_theme.font("body_bold"))
            vl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            r.addWidget(vl)
            w_r = QWidget()
            w_r.setLayout(r)
            cl.addWidget(w_r)

        content.lay.addWidget(card)

        # Результаты по урокам
        if scores:
            res_card = GlassCard()
            rl = QVBoxLayout(res_card)
            rl.setContentsMargins(int(22 * s), int(18 * s),
                                  int(22 * s), int(18 * s))
            rl.setSpacing(int(8 * s))

            rt = QLabel(i18n.t("stats_scores"))
            rt.setFont(qt_theme.font("h3"))
            rt.setStyleSheet(
                f"color: {qt_theme.c('accent')}; background: transparent;")
            rl.addWidget(rt)

            for key in sorted(scores.keys()):
                rec = scores[key]
                r = QHBoxLayout()
                k = QLabel(key)
                k.setFont(qt_theme.font("body"))
                k.setStyleSheet(
                    f"color: {qt_theme.c('text')}; background: transparent;")
                k.setFixedWidth(int(260 * s))
                r.addWidget(k)
                v = QLabel(f"{rec.get('best', 0)} / {rec.get('total', 0)}")
                v.setFont(qt_theme.font("body_bold"))
                v.setStyleSheet(
                    f"color: {qt_theme.c('success')}; background: transparent;")
                r.addWidget(v)
                r.addStretch()
                w_r = QWidget()
                w_r.setLayout(r)
                rl.addWidget(w_r)

            content.lay.addWidget(res_card)

        content.lay.addStretch()
