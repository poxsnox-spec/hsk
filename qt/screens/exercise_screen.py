# -*- coding: utf-8 -*-
"""Экран упражнений РТ — listening / reading / writing."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.widgets import (ScrollPage, GlassCard, InnerCard, PageHeader,
                        primary_btn_qss, answer_option_qss)
from core.i18n import i18n
from core.storage import storage
from core.audio import audio
from models.lesson import load_lesson


class ExerciseScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, unit, index, mode, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.unit = unit
        self.index = index
        self.mode = mode   # "listening" | "reading" | "writing"
        self.lesson = load_lesson(unit, index)
        self._build()

    # ------------------------------------------------------------
    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        # Заголовок
        if self.mode == "listening":
            title = i18n.t("wb_listening")
            questions = self.lesson.wb_listening
        elif self.mode == "reading":
            title = i18n.t("wb_reading")
            questions = self.lesson.wb_reading
        else:
            title = i18n.t("wb_writing")
            questions = self.lesson.wb_writing

        self.questions = questions
        self.score = 0
        self.q_index = 0

        header = PageHeader(
            title,
            f"Урок {self.unit}.{self.index}",
        )
        header.back_clicked.connect(self.back_requested.emit)
        root.addWidget(header)

        # Панель управления (аудио для listening)
        if self.mode == "listening":
            ctrl = QHBoxLayout()
            ctrl.setSpacing(int(8 * s))

            for key in ("workbook_01_1", "workbook_01_2",
                        f"workbook_{self.unit}{self.index}_1",
                        f"workbook_{self.unit}{self.index}_2"):
                fname = self.lesson.audio_files.get(key, "")
                if not fname:
                    continue
                has = audio.exists(self.unit, self.index, fname)
                btn = QPushButton(f"🔊 {fname}")
                btn.setEnabled(has)
                btn.setCursor(Qt.PointingHandCursor if has else Qt.ArrowCursor)
                btn.setMinimumHeight(int(36 * s))
                btn.setStyleSheet(primary_btn_qss())
                if has:
                    btn.clicked.connect(
                        lambda _c=False, u=self.unit, i=self.index, f=fname:
                        audio.play(audio.find(u, i, f))
                    )
                ctrl.addWidget(btn)
            ctrl.addStretch()
            root.addLayout(ctrl)

        # Контейнер с контентом
        if self.mode == "writing":
            self._content = self._make_writing_page()
        else:
            self._content = self._make_quiz_page()

        root.addWidget(self._content, 1)

        if self.mode != "writing":
            self._render_question()

    # ------------------------------------------------------------
    def _make_quiz_page(self):
        page = ScrollPage(self)
        return page

    def _make_writing_page(self):
        page = ScrollPage(self)
        s = qt_theme.scale

        for i, task in enumerate(self.lesson.wb_writing, 1):
            card = GlassCard()
            cl = QVBoxLayout(card)
            cl.setContentsMargins(int(22 * s), int(18 * s),
                                  int(22 * s), int(18 * s))
            cl.setSpacing(int(10 * s))

            # Заголовок
            t_lbl = QLabel(f"Задание {i}")
            ft = qt_theme.font("h3")
            t_lbl.setFont(ft)
            t_lbl.setStyleSheet(
                f"color: {qt_theme.c('accent')}; background: transparent;")
            cl.addWidget(t_lbl)

            # Промпт
            prompt = task["prompt"].get(i18n.language, "")
            p_lbl = QLabel(prompt)
            p_lbl.setWordWrap(True)
            p_lbl.setFont(qt_theme.font("body"))
            p_lbl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            cl.addWidget(p_lbl)

            if task.get("type") == "order":
                # Показываем слова вперемешку
                words = list(task.get("words", []))
                w_row = QHBoxLayout()
                for w in words:
                    w_lbl = QLabel(w)
                    fw = QFont(qt_theme._cjk)
                    fw.setPointSize(int(13 * s))
                    w_lbl.setFont(fw)
                    w_lbl.setStyleSheet(
                        f"color: {qt_theme.c('text')}; "
                        f"background-color: rgba(40, 60, 84, 150); "
                        f"border: 1px solid rgba(120, 160, 200, 70); "
                        f"border-radius: 8px; padding: 6px 12px;")
                    w_row.addWidget(w_lbl)
                w_row.addStretch()
                cl.addLayout(w_row)

                # Поле ввода
                entry = QTextEdit()
                entry.setFixedHeight(int(50 * s))
                entry.setFont(QFont(qt_theme._cjk, int(13 * s)))
                entry.setStyleSheet(f"""
                    QTextEdit {{
                        background-color: rgba(20, 30, 42, 180);
                        border: 1px solid rgba(120, 160, 200, 70);
                        border-radius: 10px;
                        color: {qt_theme.c('text')};
                        padding: 8px;
                    }}
                """)
                cl.addWidget(entry)

                # Кнопка проверки
                fb_lbl = QLabel("")
                fb_lbl.setFont(qt_theme.font("body_bold"))
                fb_lbl.setStyleSheet("background: transparent;")

                def check(entry=entry, fb=fb_lbl, task=task):
                    user = entry.toPlainText().replace(" ", "").strip()
                    correct = task["answer"].replace(" ", "")
                    if user == correct:
                        fb.setText("✓  " + i18n.t("correct"))
                        fb.setStyleSheet(
                            f"color: {qt_theme.c('success')}; "
                            f"background: transparent;")
                    else:
                        fb.setText(f"✗  {i18n.t('correct_answer')}: {task['answer']}")
                        fb.setStyleSheet(
                            f"color: {qt_theme.c('error')}; "
                            f"background: transparent;")

                btn = QPushButton(i18n.t("check"))
                btn.setCursor(Qt.PointingHandCursor)
                btn.setMinimumHeight(int(40 * s))
                btn.setStyleSheet(primary_btn_qss())
                btn.clicked.connect(check)
                cl.addWidget(btn)
                cl.addWidget(fb_lbl)

            elif task.get("type") == "essay":
                # Обязательные слова
                req = task.get("required_words", [])
                if req:
                    info = InnerCard()
                    il = QVBoxLayout(info)
                    il.setContentsMargins(int(14 * s), int(10 * s),
                                          int(14 * s), int(10 * s))
                    info_lbl = QLabel(i18n.t("wb_required_words"))
                    info_lbl.setFont(qt_theme.font("muted"))
                    info_lbl.setStyleSheet(
                        f"color: {qt_theme.c('text_muted')}; "
                        f"background: transparent;")
                    il.addWidget(info_lbl)

                    words_lbl = QLabel("  ".join(req))
                    fw = QFont(qt_theme._cjk)
                    fw.setPointSize(int(12 * s))
                    words_lbl.setFont(fw)
                    words_lbl.setStyleSheet(
                        f"color: {qt_theme.c('text')}; background: transparent;")
                    il.addWidget(words_lbl)
                    cl.addWidget(info)

                # TextEdit для эссе
                entry = QTextEdit()
                entry.setMinimumHeight(int(150 * s))
                entry.setFont(QFont(qt_theme._cjk, int(12 * s)))
                entry.setStyleSheet(f"""
                    QTextEdit {{
                        background-color: rgba(20, 30, 42, 180);
                        border: 1px solid rgba(120, 160, 200, 70);
                        border-radius: 10px;
                        color: {qt_theme.c('text')};
                        padding: 10px;
                    }}
                """)
                cl.addWidget(entry)

                fb_lbl = QLabel("")
                fb_lbl.setFont(qt_theme.font("body"))
                fb_lbl.setWordWrap(True)
                fb_lbl.setStyleSheet("background: transparent;")

                def check_essay(entry=entry, fb=fb_lbl, task=task):
                    body = entry.toPlainText().strip()
                    length = sum(1 for c in body if "\u4e00" <= c <= "\u9fff")
                    missing = [w for w in task.get("required_words", [])
                               if w not in body]
                    parts = [f"Иероглифов: {length}"]
                    min_len = task.get("min_length", 80)
                    if length < min_len:
                        parts.append(f"нужно ≥ {min_len}")
                    if missing:
                        parts.append("не хватает: " + ", ".join(missing))
                    ok = length >= min_len and not missing
                    fb.setText(("✓  " if ok else "•  ") + "; ".join(parts))
                    fb.setStyleSheet(
                        f"color: {qt_theme.c('success') if ok else qt_theme.c('warn')}; "
                        f"background: transparent;")

                btn = QPushButton(i18n.t("check"))
                btn.setCursor(Qt.PointingHandCursor)
                btn.setMinimumHeight(int(40 * s))
                btn.setStyleSheet(primary_btn_qss())
                btn.clicked.connect(check_essay)
                cl.addWidget(btn)
                cl.addWidget(fb_lbl)

            page.lay.addWidget(card)

        page.lay.addStretch()
        return page

    # ------------------------------------------------------------
    def _render_question(self):
        """Отрисовка одного вопроса квиза."""
        # Очищаем
        while self._content.lay.count():
            item = self._content.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        s = qt_theme.scale

        if self.q_index >= len(self.questions):
            self._render_finish()
            return

        q = self.questions[self.q_index]

        # Заголовок вопроса
        top = QHBoxLayout()
        num_lbl = QLabel(f"{self.q_index + 1} / {len(self.questions)}")
        num_lbl.setFont(qt_theme.font("body_bold"))
        num_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        top.addWidget(num_lbl)

        score_lbl = QLabel(f"✓ {self.score}")
        score_lbl.setFont(qt_theme.font("body_bold"))
        score_lbl.setStyleSheet(
            f"color: {qt_theme.c('success')}; background: transparent;")
        top.addStretch()
        top.addWidget(score_lbl)

        top_wrap = QWidget()
        top_wrap.setLayout(top)
        self._content.lay.addWidget(top_wrap)

        # Карточка с промптом
        prompt_card = GlassCard()
        pl = QVBoxLayout(prompt_card)
        pl.setContentsMargins(int(22 * s), int(18 * s),
                              int(22 * s), int(18 * s))

        prompt = q.prompt.get(i18n.language, "") or q.prompt.get("en", "")
        p_lbl = QLabel(prompt)
        p_lbl.setWordWrap(True)
        f = QFont(qt_theme._cjk)
        f.setPointSize(int(14 * s))
        p_lbl.setFont(f)
        p_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        pl.addWidget(p_lbl)
        self._content.lay.addWidget(prompt_card)

        # Варианты ответа
        self._option_buttons = []
        for i, opt in enumerate(q.options):
            letter = "ABCD"[i]
            btn = QPushButton(f"  {letter}.  {opt}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(int(56 * s))
            fopt = QFont(qt_theme._cjk)
            fopt.setPointSize(int(13 * s))
            btn.setFont(fopt)
            btn.setStyleSheet(answer_option_qss("idle"))
            btn.clicked.connect(
                lambda _c=False, idx=i: self._check_answer(idx)
            )
            self._content.lay.addWidget(btn)
            self._option_buttons.append(btn)

        # Feedback
        self._feedback_lbl = QLabel("")
        self._feedback_lbl.setFont(qt_theme.font("h3"))
        self._feedback_lbl.setWordWrap(True)
        self._feedback_lbl.setStyleSheet("background: transparent;")
        self._content.lay.addWidget(self._feedback_lbl)

        self._content.lay.addStretch()

    def _check_answer(self, idx):
        q = self.questions[self.q_index]
        correct = q.answer
        is_correct = (idx == correct)

        # Подсветка
        for i, btn in enumerate(self._option_buttons):
            btn.setEnabled(False)
            if i == correct:
                btn.setStyleSheet(answer_option_qss("correct"))
            elif i == idx:
                btn.setStyleSheet(answer_option_qss("wrong"))
            else:
                btn.setStyleSheet(answer_option_qss("disabled"))

        if is_correct:
            self.score += 1
            self._feedback_lbl.setText("✓  " + i18n.t("correct"))
            self._feedback_lbl.setStyleSheet(
                f"color: {qt_theme.c('success')}; background: transparent;")
        else:
            right = q.options[correct]
            self._feedback_lbl.setText(
                f"✗  {i18n.t('correct_answer')}: {right}")
            self._feedback_lbl.setStyleSheet(
                f"color: {qt_theme.c('error')}; background: transparent;")

        # Авто-переход через 1.2 сек
        QTimer.singleShot(1200, self._next_question)

    def _next_question(self):
        self.q_index += 1
        self._render_question()

    def _render_finish(self):
        s = qt_theme.scale
        storage.update_score(
            f"unit{self.unit}_lesson{self.index}_{self.mode}",
            self.score, len(self.questions)
        )

        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(40 * s), int(40 * s),
                              int(40 * s), int(40 * s))
        cl.setSpacing(int(14 * s))

        done_lbl = QLabel("🎉  " + i18n.t("quiz_session_end"))
        f = qt_theme.font("h2")
        done_lbl.setFont(f)
        done_lbl.setAlignment(Qt.AlignCenter)
        done_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(done_lbl)

        score_lbl = QLabel(f"{self.score} / {len(self.questions)}")
        fs = QFont(qt_theme._ui)
        fs.setPointSize(int(28 * s))
        fs.setBold(True)
        score_lbl.setFont(fs)
        score_lbl.setAlignment(Qt.AlignCenter)
        score_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        cl.addWidget(score_lbl)

        btns = QHBoxLayout()
        btns.addStretch()

        retry = QPushButton(i18n.t("quiz_again"))
        retry.setCursor(Qt.PointingHandCursor)
        retry.setMinimumHeight(int(44 * s))
        retry.setStyleSheet(primary_btn_qss())
        retry.clicked.connect(self._restart)
        btns.addWidget(retry)

        back = QPushButton(i18n.t("back_btn"))
        back.setCursor(Qt.PointingHandCursor)
        back.setMinimumHeight(int(44 * s))
        back.setStyleSheet(primary_btn_qss("rgba(80, 100, 130, 140)"))
        back.clicked.connect(self.back_requested.emit)
        btns.addWidget(back)

        btns.addStretch()
        cl.addLayout(btns)

        self._content.lay.addWidget(card)
        self._content.lay.addStretch()

    def _restart(self):
        self.score = 0
        self.q_index = 0
        self._render_question()
