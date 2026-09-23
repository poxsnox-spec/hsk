# -*- coding: utf-8 -*-
"""Экран урока: 8 вкладок в стиле iOS Liquid Glass."""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy,
    QScrollArea, QStackedWidget, QPushButton, QButtonGroup,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.glass import (icon_tile_qss, soft_shadow, sidebar_qss)
from core.i18n import i18n
from core.storage import storage
from core.audio import audio
from models.lesson import load_lesson


def strip_icon(text: str) -> str:
    """Убирает ведущий эмодзи из строки. '🎓 Применение' → 'Применение'."""
    text = text.strip()
    if text and ord(text[0]) > 0x2000:
        idx = text.find(" ")
        if idx > 0:
            return text[idx + 1:]
    return text


# Цвета юнитов для плитки
UNIT_COLORS = {
    1: ("rgba(74, 158, 255, 70)",  "rgba(120, 180, 255, 110)"),
    2: ("rgba(92, 214, 142, 70)",  "rgba(140, 235, 180, 110)"),
    3: ("rgba(245, 184, 73, 70)",  "rgba(255, 210, 120, 110)"),
    4: ("rgba(155, 126, 232, 70)", "rgba(190, 165, 255, 110)"),
    5: ("rgba(77, 212, 200, 70)",  "rgba(130, 230, 220, 110)"),
    6: ("rgba(240, 108, 154, 70)", "rgba(255, 150, 190, 110)"),
}


# ---------- Общие QSS ----------
def card_qss():
    return f"""
        QFrame#contentCard {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(40, 60, 84, 220),
                stop:1 rgba(22, 34, 48, 210));
            border: 1px solid rgba(120, 160, 200, 50);
            border-top: 1px solid rgba(180, 210, 240, 80);
            border-radius: 16px;
        }}
    """


def inner_card_qss():
    return f"""
        QFrame#innerCard {{
            background-color: rgba(28, 44, 62, 140);
            border: 1px solid rgba(120, 160, 200, 45);
            border-radius: 12px;
        }}
    """


def scroll_qss():
    return """
        QScrollArea { background: transparent; border: none; }
        QScrollArea > QWidget > QWidget { background: transparent; }
        QScrollBar:vertical {
            background: rgba(40, 60, 84, 100);
            width: 10px; border-radius: 5px; margin: 0;
        }
        QScrollBar::handle:vertical {
            background: rgba(120, 160, 200, 140);
            border-radius: 5px; min-height: 30px;
        }
        QScrollBar::handle:vertical:hover { background: rgba(150, 190, 230, 200); }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none; border: none;
        }
    """


def table_qss():
    return f"""
        QTableWidget {{
            background-color: transparent;
            border: none;
            gridline-color: rgba(120, 160, 200, 40);
            color: {qt_theme.c('text')};
            font-size: 11pt;
            selection-background-color: rgba(74, 158, 255, 90);
            selection-color: {qt_theme.c('text')};
        }}
        QTableWidget::item {{
            padding: 8px 6px;
            border: none;
        }}
        QHeaderView::section {{
            background-color: rgba(30, 46, 64, 200);
            color: {qt_theme.c('text')};
            padding: 10px 8px;
            border: none;
            border-bottom: 1px solid rgba(140, 180, 220, 60);
            font-weight: bold;
        }}
        QTableCornerButton::section {{
            background-color: rgba(30, 46, 64, 200);
            border: none;
        }}
    """


# ============================================================
class TabButton(QPushButton):
    """Одна кнопка-вкладка в стиле iOS segmented control."""
    def __init__(self, key: str, label: str, parent=None):
        super().__init__(label, parent)
        self.key = key
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(int(38 * qt_theme.scale))
        self.setFont(qt_theme.font("muted"))
        self._update_style(False)

    def _update_style(self, active: bool):
        if active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(74, 158, 255, 130);
                    border: 1px solid rgba(140, 190, 240, 180);
                    border-radius: 10px;
                    color: #FFFFFF;
                    font-weight: bold;
                    padding: 6px 16px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(40, 60, 84, 120);
                    border: 1px solid rgba(120, 160, 200, 40);
                    border-radius: 10px;
                    color: {qt_theme.c('text_muted')};
                    padding: 6px 16px;
                }}
                QPushButton:hover {{
                    background-color: rgba(60, 90, 120, 180);
                    border: 1px solid rgba(140, 180, 220, 90);
                    color: {qt_theme.c('text')};
                }}
            """)

    def set_active(self, active: bool):
        self.setChecked(active)
        self._update_style(active)


# ============================================================
class ScrollPage(QScrollArea):
    """Базовая прокручиваемая страница с прозрачным фоном."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(scroll_qss())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.inner = QWidget()
        self.inner.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWidget(self.inner)

        self.lay = QVBoxLayout(self.inner)
        self.lay.setContentsMargins(int(6 * qt_theme.scale),
                                     int(6 * qt_theme.scale),
                                     int(12 * qt_theme.scale),
                                     int(12 * qt_theme.scale))
        self.lay.setSpacing(int(12 * qt_theme.scale))


# ============================================================
#                   8 СТРАНИЦ
# ============================================================
class TextPage(ScrollPage):
    def __init__(self, lesson, unit, index, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        # Кнопки аудио
        audio_row = QHBoxLayout()
        audio_row.setSpacing(int(8 * s))
        for key, label in (("textbook_1", "🔊 Текст 1"),
                            ("textbook_2", "🔊 Текст 2")):
            fname = lesson.audio_files.get(key, "")
            has = bool(fname) and audio.exists(unit, index, fname)
            btn = QPushButton(label)
            btn.setEnabled(has)
            btn.setCursor(Qt.PointingHandCursor if has else Qt.ArrowCursor)
            btn.setMinimumHeight(int(36 * s))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(74, 158, 255, 70);
                    border: 1px solid rgba(140, 180, 220, 90);
                    border-radius: 10px;
                    color: {qt_theme.c('text')};
                    padding: 6px 16px;
                    font-size: 11pt;
                }}
                QPushButton:hover {{ background-color: rgba(74, 158, 255, 130); }}
                QPushButton:disabled {{
                    color: {qt_theme.c('text_muted')};
                    background-color: rgba(40, 60, 84, 80);
                }}
            """)
            if has:
                btn.clicked.connect(
                    lambda _c=False, u=unit, i=index, f=fname:
                    audio.play(audio.find(u, i, f))
                )
            audio_row.addWidget(btn)
        audio_row.addStretch()
        self.lay.addLayout(audio_row)

        # Hanzi текст
        zh_card = QFrame()
        zh_card.setObjectName("contentCard")
        zh_card.setStyleSheet(card_qss())
        zl = QVBoxLayout(zh_card)
        zl.setContentsMargins(int(24 * s), int(20 * s),
                              int(24 * s), int(20 * s))
        zh_lbl = QLabel(lesson.text_zh)
        zh_lbl.setWordWrap(True)
        f = QFont(qt_theme._cjk)
        f.setPointSize(int(13 * s))
        zh_lbl.setFont(f)
        zh_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        zh_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        zl.addWidget(zh_lbl)
        self.lay.addWidget(zh_card)

        # Перевод
        tr = lesson.text_translation.get(i18n.language, "")
        if tr:
            tr_card = QFrame()
            tr_card.setObjectName("innerCard")
            tr_card.setStyleSheet(inner_card_qss())
            tl = QVBoxLayout(tr_card)
            tl.setContentsMargins(int(20 * s), int(16 * s),
                                  int(20 * s), int(16 * s))
            tr_lbl = QLabel(tr)
            tr_lbl.setWordWrap(True)
            tr_lbl.setFont(qt_theme.font("body"))
            tr_lbl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            tr_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            tl.addWidget(tr_lbl)
            self.lay.addWidget(tr_card)

        self.lay.addStretch()


class VocabPage(ScrollPage):
    """Таблица слов урока с ОДНОЙ колонкой перевода (текущий язык)."""
    def __init__(self, lesson, unit, index, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        # Заголовок
        top = QHBoxLayout()
        top.setSpacing(int(10 * s))

        cnt = QLabel(f"生词 · {len(lesson.vocabulary)}")
        cnt.setFont(qt_theme.font("h3"))
        cnt.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        top.addWidget(cnt)
        top.addStretch()
        self.lay.addLayout(top)

        # ---- Динамические колонки: только текущий язык ----
        cur_lang = i18n.language   # ru / tk / en
        lang_header = {
            "ru": "RU",
            "tk": "TK",
            "en": "EN",
        }.get(cur_lang, "EN")

        # Заголовки: 汉字 / Pinyin / POS / <язык>
        headers = ["汉字", "Pinyin", i18n.t("vocab_col_pos"), lang_header]

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(lesson.vocabulary))
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setShowGrid(False)
        table.setAlternatingRowColors(False)
        table.setStyleSheet(table_qss())

        tf = QFont(qt_theme._cjk)
        tf.setPointSize(int(11 * s))
        table.setFont(tf)

        for row, w in enumerate(lesson.vocabulary):
            # 汉字 (accent, bold)
            item0 = QTableWidgetItem(w.hanzi)
            item0.setForeground(QColor(qt_theme.c("accent")))
            fzh = QFont(qt_theme._cjk)
            fzh.setPointSize(int(14 * s))
            fzh.setBold(True)
            item0.setFont(fzh)
            table.setItem(row, 0, item0)

            # Pinyin
            item1 = QTableWidgetItem(w.pinyin)
            item1.setForeground(QColor(qt_theme.c("text_muted")))
            table.setItem(row, 1, item1)

            # POS
            item2 = QTableWidgetItem(w.pos)
            item2.setForeground(QColor(qt_theme.c("text_muted")))
            table.setItem(row, 2, item2)

            # Перевод — только на текущем языке
            item3 = QTableWidgetItem(w.translate(cur_lang))
            item3.setForeground(QColor(qt_theme.c("text")))
            table.setItem(row, 3, item3)

        table.resizeColumnsToContents()
        hdr = table.horizontalHeader()
        hdr.setSectionResizeMode(3, QHeaderView.Stretch)
        hdr.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        table.setMinimumHeight(int(48 * s) + len(lesson.vocabulary) * int(34 * s))
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lay.addWidget(table)
        self.lay.addStretch()


class GrammarPage(ScrollPage):
    def __init__(self, lesson, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        for gp in lesson.grammar:
            card = QFrame()
            card.setObjectName("contentCard")
            card.setStyleSheet(card_qss())
            cl = QVBoxLayout(card)
            cl.setContentsMargins(int(22 * s), int(18 * s),
                                  int(22 * s), int(18 * s))
            cl.setSpacing(int(10 * s))

            # Заголовок: слово + POS
            head = QHBoxLayout()
            head.setSpacing(int(10 * s))

            word = QLabel(gp.word)
            fw = QFont(qt_theme._cjk)
            fw.setPointSize(int(22 * s))
            fw.setBold(True)
            word.setFont(fw)
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
            cl.addLayout(head)

            # Объяснение
            expl = QLabel(gp.explanation.get(i18n.language, ""))
            expl.setWordWrap(True)
            expl.setFont(qt_theme.font("body"))
            expl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            expl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            cl.addWidget(expl)

            # Примеры
            for i, ex in enumerate(gp.examples, 1):
                ex_card = QFrame()
                ex_card.setObjectName("innerCard")
                ex_card.setStyleSheet(inner_card_qss())
                el = QVBoxLayout(ex_card)
                el.setContentsMargins(int(14 * s), int(10 * s),
                                      int(14 * s), int(10 * s))
                el.setSpacing(int(4 * s))

                zh = QLabel(f"{i}. {ex.get('zh', '')}")
                fzh = QFont(qt_theme._cjk)
                fzh.setPointSize(int(12 * s))
                zh.setFont(fzh)
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

                cl.addWidget(ex_card)

            self.lay.addWidget(card)

        self.lay.addStretch()


class PhrasesPage(ScrollPage):
    def __init__(self, lesson, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        for col in lesson.collocations:
            card = QFrame()
            card.setObjectName("contentCard")
            card.setStyleSheet(card_qss())
            cl = QVBoxLayout(card)
            cl.setContentsMargins(int(22 * s), int(16 * s),
                                  int(22 * s), int(16 * s))
            cl.setSpacing(int(8 * s))

            pattern = QLabel(col.get("pattern", ""))
            fp = qt_theme.font("h3")
            pattern.setFont(fp)
            pattern.setStyleSheet(
                f"color: {qt_theme.c('accent')}; background: transparent;")
            cl.addWidget(pattern)

            for item in col.get("items", []):
                lbl = QLabel("  ·  " + item)
                f = QFont(qt_theme._cjk)
                f.setPointSize(int(12 * s))
                lbl.setFont(f)
                lbl.setWordWrap(True)
                lbl.setStyleSheet(
                    f"color: {qt_theme.c('text')}; background: transparent;")
                lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
                cl.addWidget(lbl)

            self.lay.addWidget(card)

        self.lay.addStretch()


class ComparePage(ScrollPage):
    def __init__(self, lesson, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        for cp in lesson.comparisons:
            card = QFrame()
            card.setObjectName("contentCard")
            card.setStyleSheet(card_qss())
            cl = QVBoxLayout(card)
            cl.setContentsMargins(int(22 * s), int(18 * s),
                                  int(22 * s), int(18 * s))
            cl.setSpacing(int(10 * s))

            # Заголовок A vs B
            head = QLabel(f"{cp.word_a}   vs   {cp.word_b}")
            fh = QFont(qt_theme._cjk)
            fh.setPointSize(int(18 * s))
            fh.setBold(True)
            head.setFont(fh)
            head.setAlignment(Qt.AlignCenter)
            head.setStyleSheet(
                f"color: {qt_theme.c('accent')}; background: transparent;")
            cl.addWidget(head)

            # Общие черты
            common_lbl = QLabel("≈ " + cp.common.get(i18n.language, ""))
            common_lbl.setWordWrap(True)
            common_lbl.setFont(qt_theme.font("body"))
            common_lbl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            common_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            cl.addWidget(common_lbl)

            # Различия
            for d in cp.differences:
                d_lbl = QLabel("≠ " + d.get(i18n.language, ""))
                d_lbl.setWordWrap(True)
                d_lbl.setFont(qt_theme.font("muted"))
                d_lbl.setStyleSheet(
                    f"color: {qt_theme.c('text_muted')}; background: transparent;")
                d_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
                cl.addWidget(d_lbl)

            self.lay.addWidget(card)

        self.lay.addStretch()


class ExercisePage(ScrollPage):
    """Обзор: 3 карточки — Listening / Reading / Writing."""
    def __init__(self, lesson, unit, index, parent=None, on_pick=None):
        super().__init__(parent)
        self._on_pick = on_pick
        s = qt_theme.scale

        info = QLabel(i18n.t("sec_exercise"))
        fi = qt_theme.font("h3")
        info.setFont(fi)
        info.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        self.lay.addWidget(info)

        # 3 карточки
        items = [
            ("🎧", strip_icon(i18n.t("wb_listening")), "listening",
             f"{len(lesson.wb_listening)} вопросов"),
            ("📖", strip_icon(i18n.t("wb_reading")), "reading",
             f"{len(lesson.wb_reading)} вопросов"),
            ("✍", strip_icon(i18n.t("wb_writing")), "writing",
             f"{len(lesson.wb_writing)} заданий"),
        ]
        for ic, title, mode, sub in items:
            card = QFrame()
            card.setObjectName("contentCard")
            card.setStyleSheet(card_qss())
            card.setCursor(Qt.PointingHandCursor)
            card.setMinimumHeight(int(90 * s))
            cl = QHBoxLayout(card)
            cl.setContentsMargins(int(20 * s), int(16 * s),
                                  int(24 * s), int(16 * s))
            cl.setSpacing(int(18 * s))

            ic_lbl = QLabel(ic)
            f = get_icon_font(int(28 * s))
            ic_lbl.setFont(f)
            ic_lbl.setFixedWidth(int(50 * s))
            ic_lbl.setAlignment(Qt.AlignCenter)
            ic_lbl.setStyleSheet("background: transparent;")
            cl.addWidget(ic_lbl)

            text_box = QVBoxLayout()
            text_box.setSpacing(2)
            t_lbl = QLabel(title)
            ft = qt_theme.font("card")
            t_lbl.setFont(ft)
            t_lbl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            text_box.addWidget(t_lbl)

            sub_lbl = QLabel(sub)
            fs = qt_theme.font("muted")
            sub_lbl.setFont(fs)
            sub_lbl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            text_box.addWidget(sub_lbl)
            cl.addLayout(text_box)
            cl.addStretch()

            # Клик → открывает упражнение
            if self._on_pick:
                def _click(_e, m=mode):
                    self._on_pick(unit, index, m)
                card.mousePressEvent = _click
            self.lay.addWidget(card)

        self.lay.addStretch()


class ExtensionPage(ScrollPage):
    def __init__(self, lesson, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        if lesson.expansion:
            topic = lesson.expansion.get("topic", {}).get(i18n.language, "")
            if topic:
                top = QLabel(topic)
                ft = qt_theme.font("h3")
                top.setFont(ft)
                top.setStyleSheet(
                    f"color: {qt_theme.c('text')}; background: transparent;")
                self.lay.addWidget(top)

            for w in lesson.expansion.get("words", []):
                card = QFrame()
                card.setObjectName("innerCard")
                card.setStyleSheet(inner_card_qss())
                cl = QHBoxLayout(card)
                cl.setContentsMargins(int(18 * s), int(12 * s),
                                      int(18 * s), int(12 * s))
                cl.setSpacing(int(14 * s))

                hz = QLabel(w["hanzi"])
                fh = QFont(qt_theme._cjk)
                fh.setPointSize(int(16 * s))
                fh.setBold(True)
                hz.setFont(fh)
                hz.setStyleSheet(
                    f"color: {qt_theme.c('accent')}; background: transparent;")
                hz.setFixedWidth(int(80 * s))
                cl.addWidget(hz)

                py = QLabel(w["pinyin"])
                fp = qt_theme.font("body")
                py.setFont(fp)
                py.setStyleSheet(
                    f"color: {qt_theme.c('text_muted')}; background: transparent;")
                py.setFixedWidth(int(140 * s))
                cl.addWidget(py)

                mn = QLabel(w["meaning"].get(i18n.language, ""))
                fm = qt_theme.font("body")
                mn.setFont(fm)
                mn.setWordWrap(True)
                mn.setStyleSheet(
                    f"color: {qt_theme.c('text')}; background: transparent;")
                cl.addWidget(mn, 1)

                self.lay.addWidget(card)

        self.lay.addStretch()


class ApplyPage(ScrollPage):
    def __init__(self, lesson, unit, index, parent=None):
        super().__init__(parent)
        s = qt_theme.scale

        # Карточка с вопросом
        card = QFrame()
        card.setObjectName("contentCard")
        card.setStyleSheet(card_qss())
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(22 * s), int(18 * s),
                              int(22 * s), int(18 * s))
        cl.setSpacing(int(12 * s))

        head = QLabel("🎓 " + strip_icon(i18n.t("sec_apply")))
        fh = qt_theme.font("h3")
        head.setFont(fh)
        head.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        cl.addWidget(head)

        disc = lesson.application.get("discussion", {}).get(i18n.language, "")
        if disc:
            dl = QLabel(disc)
            dl.setWordWrap(True)
            dl.setFont(qt_theme.font("body"))
            dl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            dl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            cl.addWidget(dl)

        self.lay.addWidget(card)

        # Кнопка «Отметить как пройденный»
        lesson_id = f"unit{unit}_lesson{index}"
        is_done = lesson_id in storage.get("completed_lessons", [])

        if is_done:
            done_lbl = QLabel("✓  " + strip_icon(i18n.t("lesson_is_done")))
            f = qt_theme.font("h3")
            done_lbl.setFont(f)
            done_lbl.setAlignment(Qt.AlignCenter)
            done_lbl.setStyleSheet(
                f"color: {qt_theme.c('success')}; background: transparent;"
                f"padding: 16px;")
            self.lay.addWidget(done_lbl)
        else:
            mark_btn = QPushButton(strip_icon(i18n.t("lesson_mark_done")))
            mark_btn.setCursor(Qt.PointingHandCursor)
            mark_btn.setMinimumHeight(int(52 * s))
            mark_btn.setFont(qt_theme.font("h3"))
            mark_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(92, 214, 142, 130);
                    border: 1px solid rgba(140, 235, 180, 180);
                    border-radius: 14px;
                    color: #FFFFFF;
                    padding: 12px 24px;
                }}
                QPushButton:hover {{
                    background-color: rgba(120, 230, 160, 180);
                    border: 1px solid rgba(180, 255, 210, 220);
                }}
            """)

            def _mark(_c=False):
                storage.mark_lesson_complete(lesson_id)
                # Перезагружаем вкладку
                self.lay.itemAt(self.lay.count() - 1).widget().deleteLater()                     if False else None
                QMessageBox.information(
                    None, "✓",
                    i18n.t("lesson_is_done")
                )
            mark_btn.clicked.connect(_mark)
            self.lay.addWidget(mark_btn)

        self.lay.addStretch()


# ============================================================
class LessonViewScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, unit, index, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.unit = unit
        self.index = index
        self.lesson = load_lesson(unit, index)
        self._tab_buttons = {}
        self._build()

    # ------------------------------------------------------------
    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        # ============ ВЕРХНЯЯ ПАНЕЛЬ ============
        top = QHBoxLayout()
        top.setSpacing(int(14 * s))

        # Назад
        back = QPushButton()
        back.setCursor(Qt.PointingHandCursor)
        back.setFixedSize(int(110 * s), int(40 * s))
        back.setText(f"  {icon('chevron')}   {i18n.t('back_btn')}")
        back.setFont(get_icon_font(int(13 * s)))
        back.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(40, 60, 84, 180);
                border: 1px solid rgba(140, 180, 220, 70);
                border-radius: 10px;
                color: {qt_theme.c('text')};
            }}
            QPushButton:hover {{
                background-color: rgba(60, 90, 120, 220);
                border: 1px solid {qt_theme.c('accent')};
            }}
        """)
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        # Плитка с номером
        color, border = UNIT_COLORS.get(self.unit, UNIT_COLORS[1])
        num_tile = QFrame()
        num_tile.setObjectName("iconTile")
        num_tile.setFixedSize(int(48 * s), int(48 * s))
        num_tile.setStyleSheet(icon_tile_qss(color, border,
                                              radius=int(12 * s)))
        nl = QVBoxLayout(num_tile)
        nl.setContentsMargins(0, 0, 0, 0)
        nl.setAlignment(Qt.AlignCenter)
        num_lbl = QLabel(f"{self.unit}.{self.index}")
        fnum = qt_theme.font("card")
        fnum.setPointSize(int(14 * s))
        num_lbl.setFont(fnum)
        num_lbl.setAlignment(Qt.AlignCenter)
        num_lbl.setStyleSheet("background: transparent; color: #FFFFFF;")
        nl.addWidget(num_lbl)
        top.addWidget(num_tile)

        # Заголовок урока
        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        zh_title = QLabel(self.lesson.title.get("zh", ""))
        fzh = QFont(qt_theme._cjk)
        fzh.setPointSize(int(20 * s))
        fzh.setBold(True)
        zh_title.setFont(fzh)
        zh_title.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        title_box.addWidget(zh_title)

        tr_title = QLabel(self.lesson.title_in(i18n.language))
        ftr = qt_theme.font("muted")
        tr_title.setFont(ftr)
        tr_title.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        title_box.addWidget(tr_title)

        top.addLayout(title_box)
        top.addStretch()
        root.addLayout(top)

        # ============ TAB BAR ============
        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(int(6 * s))

        tabs = [
            ("text",     i18n.t("sec_text")),
            ("vocab",    i18n.t("sec_vocab")),
            ("grammar",  i18n.t("sec_grammar")),
            ("phrases",  i18n.t("sec_phrases")),
            ("compare",  i18n.t("sec_compare")),
            ("exercise", i18n.t("sec_exercise")),
            ("extend",   i18n.t("sec_extend")),
            ("apply",    i18n.t("sec_apply")),
        ]

        self._stack = QStackedWidget()
        self._stack.setAttribute(Qt.WA_TranslucentBackground, True)

        # Создаём страницы
        # Получаем callback от MainWindow
        on_exercise = getattr(self, "exercise_requested", None)

        pages = {
            "text":     TextPage(self.lesson, self.unit, self.index),
            "vocab":    VocabPage(self.lesson, self.unit, self.index),
            "grammar":  GrammarPage(self.lesson),
            "phrases":  PhrasesPage(self.lesson),
            "compare":  ComparePage(self.lesson),
            "exercise": ExercisePage(self.lesson, self.unit, self.index,
                                      on_pick=on_exercise),
            "extend":   ExtensionPage(self.lesson),
            "apply":    ApplyPage(self.lesson, self.unit, self.index),
        }

        for key, label in tabs:
            page = pages[key]
            self._stack.addWidget(page)

            btn = TabButton(key, label, parent=self)
            btn.clicked.connect(lambda _c=False, k=key: self._on_tab_click(k))
            tabs_row.addWidget(btn)
            self._tab_buttons[key] = btn

        tabs_row.addStretch()
        root.addLayout(tabs_row)

        # ============ КОНТЕНТ ============
        root.addWidget(self._stack, 1)

        # Активируем первую вкладку
        self._on_tab_click("text")

    # ------------------------------------------------------------
    def _on_tab_click(self, key: str):
        # Обновляем активное состояние
        for k, btn in self._tab_buttons.items():
            btn.set_active(k == key)
        # Показываем нужную страницу
        keys = list(self._tab_buttons.keys())
        idx = keys.index(key)
        self._stack.setCurrentIndex(idx)
