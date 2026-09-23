# -*- coding: utf-8 -*-
"""Список уроков — непрозрачные карточки, чистый скролл."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QSizePolicy, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.glass import opaque_card_qss, opaque_icon_tile_qss
from qt.widgets import OpaqueScrollPage, BackButton, scroll_bg_color
from core.i18n import i18n
from core.config import UNIT_TITLES
from core.storage import storage


def _load_lesson_titles():
    """Загружает названия уроков из JSON — единый источник правды."""
    import json as _json
    from pathlib import Path as _Path
    base = _Path(__file__).resolve().parent.parent.parent / "data" / "lessons"
    titles = {}
    for u in range(1, 7):
        for i in range(1, 4):
            p = base / f"unit{u}" / f"lesson{i:02d}.json"
            if not p.exists():
                continue
            try:
                d = _json.loads(p.read_text(encoding="utf-8"))
                titles[(u, i)] = d.get("title", {})
            except Exception:
                pass
    return titles


LESSON_TITLES = _load_lesson_titles()


# НЕпрозрачные цвета юнитов (hex, без alpha)
UNIT_COLORS = {
    1: ("#3A6088", "#5A80A8"),   # синий
    2: ("#3A7060", "#5A9080"),   # зелёный
    3: ("#7A6030", "#9A8050"),   # оранжевый
    4: ("#5A4A88", "#7A6AA8"),   # фиолетовый
    5: ("#3A7080", "#5A90A0"),   # бирюза
    6: ("#7A3A60", "#9A5A80"),   # розовый
}


class LessonRow(QFrame):
    clicked = pyqtSignal(int, int)

    def __init__(self, unit, index, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.index = index

        self.setObjectName("glassCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(int(72 * qt_theme.scale))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(opaque_card_qss())

        s = qt_theme.scale
        is_done = f"unit{unit}_lesson{index}" in storage.get("completed_lessons", [])

        lay = QHBoxLayout(self)
        lay.setContentsMargins(int(18 * s), int(12 * s),
                               int(20 * s), int(12 * s))
        lay.setSpacing(int(16 * s))

        # Плитка номера — непрозрачная
        num_tile = QFrame()
        num_tile.setObjectName("iconTile")
        num_tile.setFixedSize(int(48 * s), int(48 * s))
        num_tile.setAttribute(Qt.WA_StyledBackground, True)
        num_tile.setAttribute(Qt.WA_OpaquePaintEvent, True)
        color, border = UNIT_COLORS.get(unit, UNIT_COLORS[1])
        num_tile.setStyleSheet(opaque_icon_tile_qss(color, border,
                                                     radius=int(12 * s)))
        nl = QVBoxLayout(num_tile)
        nl.setContentsMargins(0, 0, 0, 0)
        nl.setAlignment(Qt.AlignCenter)
        num_lbl = QLabel(f"{unit}.{index}")
        f_num = qt_theme.font("card")
        f_num.setPointSize(int(14 * qt_theme.scale))
        num_lbl.setFont(f_num)
        num_lbl.setAlignment(Qt.AlignCenter)
        num_lbl.setStyleSheet("background: transparent; color: #FFFFFF;")
        nl.addWidget(num_lbl)
        lay.addWidget(num_tile)

        # Текст
        text_box = QVBoxLayout()
        text_box.setSpacing(int(2 * s))

        titles = LESSON_TITLES.get((unit, index), {})
        zh = titles.get("zh", f"Урок {unit}.{index}")
        zh_lbl = QLabel(zh)
        zh_lbl.setFont(qt_theme.font("h3"))
        zh_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        text_box.addWidget(zh_lbl)

        tr = titles.get(i18n.language, titles.get("en", ""))
        tr_lbl = QLabel(tr)
        tr_lbl.setFont(qt_theme.font("muted"))
        tr_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        text_box.addWidget(tr_lbl)

        lay.addLayout(text_box)
        lay.addStretch()

        # Статус
        if is_done:
            status = QLabel(icon("check"))
            status.setFont(get_icon_font(int(18 * s)))
            status.setFixedWidth(int(24 * s))
            status.setAlignment(Qt.AlignCenter)
            status.setStyleSheet(
                f"color: {qt_theme.c('success')}; background: transparent;")
            lay.addWidget(status)
        else:
            spacer = QLabel("")
            spacer.setFixedWidth(int(24 * s))
            lay.addWidget(spacer)

        # Chevron
        self.chevron = QLabel(icon("chevron"))
        self.chevron.setFont(get_icon_font(int(18 * s)))
        self.chevron.setFixedWidth(int(22 * s))
        self.chevron.setAlignment(Qt.AlignCenter)
        self.chevron.setStyleSheet(
            "color: rgba(140, 180, 220, 200); background: transparent;")
        lay.addWidget(self.chevron)

    def enterEvent(self, event):
        self.chevron.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.chevron.setStyleSheet(
            "color: rgba(140, 180, 220, 200); background: transparent;")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.unit, self.index)
        super().mousePressEvent(event)


class LessonMenuScreen(QWidget):
    back_requested = pyqtSignal()
    lesson_open = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        # НЕ используем WA_TranslucentBackground — иначе фоновый паттерн
        # просвечивает сквозь скролл и создаёт ghosting
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)
        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        # Верхняя панель
        top = QHBoxLayout()
        top.setSpacing(int(14 * s))

        back = BackButton(i18n.t("back_btn"))
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        title = QLabel(i18n.t("lessons_title"))
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        title_box.addWidget(title)

        sub = QLabel(i18n.t("lessons_sub"))
        sub.setFont(qt_theme.font("muted"))
        sub.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        title_box.addWidget(sub)

        top.addLayout(title_box)
        top.addStretch()
        root.addLayout(top)

        # Скролл-страница — OpaqueScrollPage
        scroll = OpaqueScrollPage()
        root.addWidget(scroll, 1)

        # 6 юнитов
        for unit in range(1, 7):
            scroll.lay.addWidget(self._make_unit_block(unit))

        scroll.lay.addStretch()

    def _make_unit_block(self, unit: int) -> QFrame:
        s = qt_theme.scale
        block = QFrame()
        # НЕпрозрачный фон блока — того же цвета, что фон скролла
        block.setAttribute(Qt.WA_StyledBackground, True)
        block.setAutoFillBackground(False)
        block.setStyleSheet(
            f"QFrame {{ background-color: {scroll_bg_color()}; "
            f"border: none; }}"
        )

        lay = QVBoxLayout(block)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(int(10 * s))

        # Заголовок юнита
        head = QHBoxLayout()
        head.setSpacing(int(10 * s))

        unit_lbl = QLabel(f"{i18n.t('unit_label').upper()} {unit}")
        f = qt_theme.font("muted")
        f.setBold(True)
        unit_lbl.setFont(f)
        unit_lbl.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        head.addWidget(unit_lbl)

        title_data = UNIT_TITLES.get(unit, {})
        zh = title_data.get("zh", "")
        tr = title_data.get(i18n.language, title_data.get("en", ""))

        name = QLabel(f"{zh}  ·  {tr}")
        name.setFont(qt_theme.font("body"))
        name.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        head.addWidget(name)
        head.addStretch()
        lay.addLayout(head)

        # 3 урока
        for idx in range(1, 4):
            row = LessonRow(unit, idx, parent=self)
            row.clicked.connect(self.lesson_open.emit)
            lay.addWidget(row)

        return block
