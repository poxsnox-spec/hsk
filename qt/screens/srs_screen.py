# -*- coding: utf-8 -*-
"""SRS с селектором урока/юнита."""
import random
from datetime import datetime

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.widgets import (OpaqueScrollPage, BackButton, scroll_bg_color,
                        primary_btn_qss, answer_option_qss, GlassCard,
                        InnerCard)
from core.i18n import i18n
from core.storage import (storage, RATING_AGAIN, RATING_HARD,
                          RATING_GOOD, RATING_EASY)
from core.audio import audio
from models.lesson import load_lesson


# SESSION_SIZE берётся из storage при каждой сессии


def fmt_interval(due_iso):
    try:
        due = datetime.fromisoformat(due_iso)
    except Exception:
        return ""
    delta = due - datetime.now()
    secs = int(delta.total_seconds())
    if secs <= 30:
        return "сейчас"
    if secs < 3600:
        return f"через {max(1, secs // 60)} мин"
    if secs < 86400 * 2:
        return f"через {max(1, secs // 3600)} ч"
    return f"через {max(1, secs // 86400)} дн."


class SrsScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)

        # Загружаем ВСЕ слова один раз
        self.all_words = []   # list of (unit, idx, w)
        for unit in range(1, 7):
            for idx in range(1, 4):
                try:
                    lesson = load_lesson(unit, idx)
                except Exception:
                    continue
                for w in lesson.vocabulary:
                    self.all_words.append((unit, idx, w))

        # Текущая область: (unit_filter, lesson_filter)
        # unit_filter=None → все юниты
        # unit_filter=1, lesson_filter=None → только Юнит 1
        # unit_filter=1, lesson_filter=2 → только урок 1.2
        self._scope_unit = None
        self._scope_lesson = None

        # Состояние сессии
        self._queue = []
        self._index = 0
        self._correct = 0
        self._flipped = False
        self._current = None

        self._build()

    # ============================================================
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

        title = QLabel(i18n.t("srs_title"))
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        top.addWidget(title)
        top.addStretch()
        root.addLayout(top)

        # Селектор области
        scope_row = self._make_scope_selector()
        root.addLayout(scope_row)

        # Контент
        self._content = OpaqueScrollPage()
        root.addWidget(self._content, 1)

        self._render_home()

    # ============================================================
    def _make_scope_selector(self):
        """Строка с двумя выпадающими списками: юнит + урок."""
        s = qt_theme.scale
        row = QHBoxLayout()
        row.setSpacing(int(10 * s))

        lbl = QLabel(i18n.t("srs_scope") + ":")
        lbl.setFont(qt_theme.font("body"))
        lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        row.addWidget(lbl)

        combo_qss = f"""
            QComboBox {{
                background-color: rgba(30, 46, 62, 220);
                border: 1px solid rgba(120, 160, 200, 80);
                border-radius: 10px;
                padding: 6px 14px;
                color: {qt_theme.c('text')};
                min-height: 36px;
            }}
            QComboBox:hover {{ border: 1px solid {qt_theme.c('accent')}; }}
            QComboBox::drop-down {{ border: none; width: 28px; }}
            QComboBox QAbstractItemView {{
                background-color: rgba(20, 34, 48, 250);
                border: 1px solid rgba(120, 160, 200, 80);
                color: {qt_theme.c('text')};
                selection-background-color: rgba(74, 158, 255, 120);
            }}
        """

        # Выпадающий список юнитов
        self.unit_combo = QComboBox()
        self.unit_combo.setFont(QFont(qt_theme._ui, int(11 * s)))
        self.unit_combo.setStyleSheet(combo_qss)
        self.unit_combo.setMinimumWidth(int(140 * s))
        self.unit_combo.addItem(i18n.t("srs_scope_all"), None)
        for u in range(1, 7):
            self.unit_combo.addItem(i18n.t("srs_scope_unit").format(n=u), u)
        self.unit_combo.currentIndexChanged.connect(self._on_unit_changed)
        row.addWidget(self.unit_combo)

        # Выпадающий список уроков
        self.lesson_combo = QComboBox()
        self.lesson_combo.setFont(QFont(qt_theme._ui, int(11 * s)))
        self.lesson_combo.setStyleSheet(combo_qss)
        self.lesson_combo.setMinimumWidth(int(180 * s))
        self.lesson_combo.addItem(i18n.t("srs_scope_all"), None)
        self.lesson_combo.currentIndexChanged.connect(self._on_lesson_changed)
        row.addWidget(self.lesson_combo)

        row.addStretch()
        return row

    def _on_unit_changed(self, idx):
        unit = self.unit_combo.itemData(idx)
        self._scope_unit = unit

        # Обновляем список уроков
        self.lesson_combo.blockSignals(True)
        self.lesson_combo.clear()
        self.lesson_combo.addItem(i18n.t("srs_scope_all"), None)

        if unit is None:
            # Все уроки: показываем все доступные
            for u in range(1, 7):
                for l in range(1, 4):
                    self.lesson_combo.addItem(
                        f"{u}.{l}", (u, l)
                    )
        else:
            for l in range(1, 4):
                self.lesson_combo.addItem(
                    i18n.t("srs_scope_lesson").format(n=f"{unit}.{l}"),
                    (unit, l)
                )
        self.lesson_combo.blockSignals(False)

        # Сбрасываем фильтр урока
        self._scope_lesson = None
        self.lesson_combo.setCurrentIndex(0)
        self._render_home()

    def _on_lesson_changed(self, idx):
        data = self.lesson_combo.itemData(idx)
        if isinstance(data, tuple):
            self._scope_unit, self._scope_lesson = data
        else:
            self._scope_lesson = None
        self._render_home()

    # ============================================================
    def _filtered_words(self):
        """Возвращает список слов, попадающих в текущую область."""
        out = []
        for unit, idx, w in self.all_words:
            if self._scope_unit is not None and unit != self._scope_unit:
                continue
            if self._scope_lesson is not None and idx != self._scope_lesson:
                continue
            out.append((unit, idx, w))
        return out

    def _due_words(self):
        """Из отфильтрованных — только те, у кого due <= сейчас."""
        due_hanzi = set(storage.srs_due())
        out = []
        for unit, idx, w in self._filtered_words():
            if w.hanzi in due_hanzi:
                out.append((unit, idx, w))
        return out

    # ============================================================
    def _clear(self):
        while self._content.lay.count():
            item = self._content.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _render_home(self):
        self._clear()
        s = qt_theme.scale

        # Статистика области
        scoped_words = self._filtered_words()
        due = self._due_words()
        known = sum(1 for _, _, w in scoped_words
                    if storage.srs_get(w.hanzi))
        streak = storage.get("streak_days", 0)

        # Сводка
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(22 * s), int(18 * s),
                              int(22 * s), int(18 * s))
        cl.setSpacing(int(10 * s))

        title = QLabel("📊  " + i18n.t("srs_title"))
        ft = qt_theme.font("h3")
        title.setFont(ft)
        title.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(title)

        rows = [
            ("⏰ " + i18n.t("srs_due_now"), str(len(due))),
            ("📖 " + i18n.t("srs_known"),
             f"{known} / {len(scoped_words)}"),
            ("🔥 Streak", f"{streak} дней"),
        ]
        for lbl_txt, val in rows:
            r = QHBoxLayout()
            k = QLabel(lbl_txt)
            k.setFont(qt_theme.font("body"))
            k.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            r.addWidget(k)
            r.addStretch()
            v = QLabel(val)
            v.setFont(qt_theme.font("body_bold"))
            v.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            r.addWidget(v)
            wrap = QWidget()
            wrap.setLayout(r)
            cl.addWidget(wrap)

        self._content.lay.addWidget(card)

        # Кнопка старта / сообщение «нет слов»
        if not due:
            info = QLabel(i18n.t("srs_scope_empty"))
            info.setFont(qt_theme.font("h3"))
            info.setAlignment(Qt.AlignCenter)
            info.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; "
                f"background-color: rgba(30, 46, 62, 180); "
                f"border: 1px solid rgba(120, 160, 200, 60); "
                f"border-radius: 12px; "
                f"padding: 20px;")
            self._content.lay.addWidget(info)
        else:
            start_btn = QPushButton(i18n.t("srs_start"))
            start_btn.setCursor(Qt.PointingHandCursor)
            start_btn.setMinimumHeight(int(56 * s))
            start_btn.setStyleSheet(primary_btn_qss("rgba(77, 212, 200, 160)"))
            start_btn.clicked.connect(self._start_session)
            self._content.lay.addWidget(start_btn)

        self._content.lay.addStretch()

    # ============================================================
    def _start_session(self):
        due = self._due_words()
        random.shuffle(due)
        session_size = storage.get('srs_session_size', 20)
        self._queue = due[:session_size]
        self._index = 0
        self._correct = 0

        if not self._queue:
            self._render_home()
            return
        self._render_card()

    # ============================================================
    def _render_card(self):
        self._clear()
        self._flipped = False
        s = qt_theme.scale

        if self._index >= len(self._queue):
            self._render_finish()
            return

        unit, lesson_idx, w = self._queue[self._index]
        self._current = (unit, lesson_idx, w)

        # Верх
        top = QHBoxLayout()
        num = QLabel(f"{self._index + 1} / {len(self._queue)}")
        num.setFont(qt_theme.font("body_bold"))
        num.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        top.addWidget(num)
        top.addStretch()
        sc = QLabel(f"✓ {self._correct}")
        sc.setFont(qt_theme.font("body_bold"))
        sc.setStyleSheet(
            f"color: {qt_theme.c('success')}; background: transparent;")
        top.addWidget(sc)
        top_w = QWidget()
        top_w.setLayout(top)
        self._content.lay.addWidget(top_w)

        # Карточка
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(40 * s), int(60 * s),
                              int(40 * s), int(60 * s))
        cl.setSpacing(int(20 * s))

        self._hanzi_lbl = QLabel(w.hanzi)
        fh = QFont(qt_theme._cjk)
        fh.setPointSize(int(72 * s))
        fh.setBold(True)
        self._hanzi_lbl.setFont(fh)
        self._hanzi_lbl.setAlignment(Qt.AlignCenter)
        self._hanzi_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        cl.addWidget(self._hanzi_lbl)

        self._pinyin_lbl = QLabel("")
        fp = QFont("Arial", int(18 * s))
        self._pinyin_lbl.setFont(fp)
        self._pinyin_lbl.setAlignment(Qt.AlignCenter)
        self._pinyin_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(self._pinyin_lbl)

        self._trans_lbl = QLabel("")
        ft = qt_theme.font("h3")
        self._trans_lbl.setFont(ft)
        self._trans_lbl.setAlignment(Qt.AlignCenter)
        self._trans_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        cl.addWidget(self._trans_lbl)

        self._content.lay.addWidget(card)

        # Кнопка «Показать»
        self._btn_wrap = QWidget()
        bw_lay = QHBoxLayout(self._btn_wrap)
        bw_lay.setContentsMargins(0, 0, 0, 0)

        self._show_btn = QPushButton(i18n.t("srs_show"))
        self._show_btn.setCursor(Qt.PointingHandCursor)
        self._show_btn.setMinimumHeight(int(56 * s))
        self._show_btn.setStyleSheet(primary_btn_qss())
        self._show_btn.clicked.connect(self._reveal)
        bw_lay.addWidget(self._show_btn)

        self._content.lay.addWidget(self._btn_wrap)
        self._content.lay.addStretch()

        # Аудио
        af = getattr(w, "audio", "") or ""
        if af and audio.exists(unit, lesson_idx, af):
            audio_btn = QPushButton("🔊")
            audio_btn.setCursor(Qt.PointingHandCursor)
            audio_btn.setFixedHeight(int(40 * s))
            audio_btn.setStyleSheet(primary_btn_qss("rgba(74, 158, 255, 120)"))
            audio_btn.clicked.connect(
                lambda _c=False, u=unit, i=lesson_idx, f=af:
                audio.play(audio.find(u, i, f))
            )
            self._content.lay.addWidget(audio_btn)

    def _reveal(self):
        if self._flipped:
            return
        self._flipped = True
        unit, li, w = self._current
        self._pinyin_lbl.setText(w.pinyin)
        self._trans_lbl.setText(w.translate(i18n.language))

        # Заменяем кнопку «Показать» на 4 кнопки оценки
        self._show_btn.setParent(None)
        s = qt_theme.scale

        row = QHBoxLayout()
        row.setSpacing(int(6 * s))
        ratings = [
            (i18n.t("srs_again"), RATING_AGAIN, "rgba(255, 108, 108, 160)"),
            (i18n.t("srs_hard"),  RATING_HARD,  "rgba(255, 160, 60, 160)"),
            (i18n.t("srs_good"),  RATING_GOOD,  "rgba(92, 214, 142, 160)"),
            (i18n.t("srs_easy"),  RATING_EASY,  "rgba(74, 158, 255, 160)"),
        ]
        for txt, r, color in ratings:
            b = QPushButton(txt)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(int(56 * s))
            b.setStyleSheet(primary_btn_qss(color))
            b.clicked.connect(lambda _c=False, rating=r: self._answer(rating))
            row.addWidget(b)

        w_row = QWidget()
        w_row.setLayout(row)
        self._content.lay.insertWidget(self._content.lay.count() - 1, w_row)

    def _answer(self, rating):
        unit, li, w = self._current
        storage.srs_review(w.hanzi, rating)
        correct = rating != RATING_AGAIN
        storage.record_word(w.hanzi, correct)
        if correct:
            self._correct += 1
        self._index += 1
        self._render_card()

    # ============================================================
    def _render_finish(self):
        s = qt_theme.scale
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(40 * s), int(40 * s),
                              int(40 * s), int(40 * s))
        cl.setSpacing(int(14 * s))

        done = QLabel("🎉  " + i18n.t("srs_finish"))
        f = qt_theme.font("h2")
        done.setFont(f)
        done.setAlignment(Qt.AlignCenter)
        done.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(done)

        score = QLabel(f"{self._correct} / {len(self._queue)}")
        fs = QFont(qt_theme._ui)
        fs.setPointSize(int(28 * s))
        fs.setBold(True)
        score.setFont(fs)
        score.setAlignment(Qt.AlignCenter)
        score.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        cl.addWidget(score)

        again = QPushButton(i18n.t("srs_another"))
        again.setCursor(Qt.PointingHandCursor)
        again.setMinimumHeight(int(48 * s))
        again.setStyleSheet(primary_btn_qss())
        again.clicked.connect(self._render_home)
        cl.addWidget(again)

        self._content.lay.addWidget(card)
        self._content.lay.addStretch()
