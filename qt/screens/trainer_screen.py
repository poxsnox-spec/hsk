# -*- coding: utf-8 -*-
"""Тренажёр: 3 режима."""
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from qt.theme import qt_theme
from qt.widgets import (ScrollPage, GlassCard, PageHeader,
                        primary_btn_qss, answer_option_qss)
from core.i18n import i18n
from core.storage import storage
from core.audio import audio
from models.lesson import load_lesson


class TrainerScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, unit, index, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.unit = unit
        self.index = index
        self.lesson = load_lesson(unit, index)
        self.mode = "hanzi_to_tr"
        self.score = 0
        self.total = 0
        self.streak = 0
        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        header = PageHeader(i18n.t("menu_trainer"),
                             f"Урок {self.unit}.{self.index}")
        header.back_clicked.connect(self.back_requested.emit)
        root.addWidget(header)

        # Режимы
        modes_row = QHBoxLayout()
        modes_row.setSpacing(int(8 * s))
        self._mode_btns = {}
        modes = [
            ("hanzi_to_tr", i18n.t("quiz_hanzi_to_translation")),
            ("tr_to_hanzi", i18n.t("quiz_translation_to_hanzi")),
            ("pinyin_to_hanzi", i18n.t("quiz_pinyin_to_hanzi")),
        ]
        for key, label in modes:
            b = QPushButton(label)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(int(42 * s))
            b.clicked.connect(lambda _c=False, k=key: self._set_mode(k))
            modes_row.addWidget(b)
            self._mode_btns[key] = b

        modes_row.addStretch()
        modes_w = QWidget()
        modes_w.setLayout(modes_row)
        root.addWidget(modes_w)

        # Контент
        self._content = ScrollPage(self)
        root.addWidget(self._content, 1)

        self._update_mode_buttons()
        self._next_question()

    def _update_mode_buttons(self):
        for k, b in self._mode_btns.items():
            if k == self.mode:
                b.setStyleSheet(primary_btn_qss())
            else:
                b.setStyleSheet(primary_btn_qss("rgba(40, 60, 84, 150)"))

    def _set_mode(self, key):
        self.mode = key
        self.score = 0
        self.total = 0
        self.streak = 0
        self._update_mode_buttons()
        self._next_question()

    def _clear(self):
        while self._content.lay.count():
            item = self._content.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _next_question(self):
        self._clear()
        s = qt_theme.scale

        word = random.choice(self.lesson.vocabulary)
        self._correct = word
        pool = [w for w in self.lesson.vocabulary if w.hanzi != word.hanzi]
        wrong = random.sample(pool, min(3, len(pool)))
        options = [word] + wrong
        random.shuffle(options)

        # Верхняя строка
        top = QHBoxLayout()
        sc = QLabel(f"✓ {self.score} / {self.total}")
        sc.setFont(qt_theme.font("body_bold"))
        sc.setStyleSheet(
            f"color: {qt_theme.c('success')}; background: transparent;")
        top.addWidget(sc)
        st = QLabel(f"🔥 {self.streak}")
        st.setFont(qt_theme.font("body_bold"))
        st.setStyleSheet(
            f"color: {qt_theme.c('warn')}; background: transparent;")
        top.addStretch()
        top.addWidget(st)
        top_w = QWidget()
        top_w.setLayout(top)
        self._content.lay.addWidget(top_w)

        # Карточка-вопрос
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(40 * s), int(40 * s),
                              int(40 * s), int(40 * s))

        if self.mode == "hanzi_to_tr":
            q_text = word.hanzi
            q_font = QFont(qt_theme._cjk)
            q_font.setPointSize(int(72 * s))
            q_font.setBold(True)
            sub = word.pinyin
            btn_text = lambda w: w.translate(i18n.language)
            btn_font = QFont(qt_theme._ui, int(13 * s))

        elif self.mode == "tr_to_hanzi":
            q_text = word.translate(i18n.language)
            q_font = qt_theme.font("h1")
            sub = ""
            btn_text = lambda w: w.hanzi
            btn_font = QFont(qt_theme._cjk, int(16 * s))

        else:   # pinyin_to_hanzi
            q_text = word.pinyin
            q_font = QFont("Arial", int(48 * s))
            q_font.setBold(True)
            sub = ""
            btn_text = lambda w: w.hanzi
            btn_font = QFont(qt_theme._cjk, int(16 * s))

        q_lbl = QLabel(q_text)
        q_lbl.setFont(q_font)
        q_lbl.setAlignment(Qt.AlignCenter)
        q_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        cl.addWidget(q_lbl)

        if sub:
            s_lbl = QLabel(sub)
            fp = QFont("Arial", int(16 * s))
            s_lbl.setFont(fp)
            s_lbl.setAlignment(Qt.AlignCenter)
            s_lbl.setStyleSheet(
                f"color: {qt_theme.c('accent')}; background: transparent;")
            cl.addWidget(s_lbl)

        self._content.lay.addWidget(card)

        # Опции
        self._option_btns = []
        for opt in options:
            b = QPushButton(btn_text(opt))
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(int(60 * s))
            b.setFont(btn_font)
            b.setStyleSheet(answer_option_qss("idle"))
            b.clicked.connect(lambda _c=False, o=opt: self._check(o))
            self._content.lay.addWidget(b)
            self._option_btns.append((b, opt))

        # Feedback
        self._feedback = QLabel("")
        self._feedback.setFont(qt_theme.font("h3"))
        self._feedback.setAlignment(Qt.AlignCenter)
        self._feedback.setStyleSheet("background: transparent;")
        self._content.lay.addWidget(self._feedback)

        self._content.lay.addStretch()

    def _check(self, chosen):
        self.total += 1
        is_correct = (chosen.hanzi == self._correct.hanzi)

        for b, opt in self._option_btns:
            b.setEnabled(False)
            if opt.hanzi == self._correct.hanzi:
                b.setStyleSheet(answer_option_qss("correct"))
            elif opt.hanzi == chosen.hanzi:
                b.setStyleSheet(answer_option_qss("wrong"))
            else:
                b.setStyleSheet(answer_option_qss("disabled"))

        if is_correct:
            self.score += 1
            self.streak += 1
            self._feedback.setText("✓ " + i18n.t("correct"))
            self._feedback.setStyleSheet(
                f"color: {qt_theme.c('success')}; background: transparent;")
        else:
            self.streak = 0
            self._feedback.setText(
                f"✗ {i18n.t('correct_answer')}: "
                f"{self._correct.hanzi}  ({self._correct.pinyin})")
            self._feedback.setStyleSheet(
                f"color: {qt_theme.c('error')}; background: transparent;")

        storage.record_word(self._correct.hanzi, is_correct)

        from PyQt5.QtCore import QTimer
        QTimer.singleShot(900, self._next_question)
