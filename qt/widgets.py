# -*- coding: utf-8 -*-
"""Компоненты с ЯВНОЙ очисткой фона — фикс ghosting при скролле."""
from PyQt5.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QWidget, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon


def scroll_bg_color() -> str:
    bg = qt_theme.c("bg")
    if bg.startswith("#"):
        return bg
    return "#0A1018"


def soft_shadow(widget, **kwargs):
    return


def card_qss():
    return f"""
        QFrame#glassCard {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(40, 60, 84, 240),
                stop:1 rgba(22, 34, 48, 235));
            border: 1px solid rgba(120, 160, 200, 80);
            border-top: 1px solid rgba(180, 210, 240, 110);
            border-radius: 16px;
        }}
        QFrame#glassCard QLabel {{ background: transparent; }}
    """


def inner_card_qss():
    return """
        QFrame#innerCard {
            background-color: rgba(28, 44, 62, 200);
            border: 1px solid rgba(120, 160, 200, 70);
            border-radius: 12px;
        }
        QFrame#innerCard QLabel { background: transparent; }
    """


def scroll_qss():
    bg = scroll_bg_color()
    return f"""
        QScrollArea {{
            background-color: {bg};
            border: none;
        }}
        QScrollArea > QWidget > QWidget {{
            background-color: {bg};
        }}
        QScrollBar:vertical {{
            background: rgba(40, 60, 84, 140);
            width: 10px; border-radius: 5px; margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: rgba(120, 160, 200, 170);
            border-radius: 5px; min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{ background: rgba(150, 190, 230, 230); }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            background: none; border: none;
        }}
    """


def primary_btn_qss(color="rgba(74, 158, 255, 140)"):
    return f"""
        QPushButton {{
            background-color: {color};
            border: 1px solid rgba(140, 190, 240, 180);
            border-radius: 12px;
            color: #FFFFFF;
            font-weight: bold;
            padding: 12px 24px;
            font-size: 13pt;
        }}
        QPushButton:hover {{
            background-color: rgba(100, 180, 255, 200);
            border: 1px solid rgba(180, 220, 255, 220);
        }}
        QPushButton:disabled {{
            background-color: rgba(60, 80, 100, 100);
            color: rgba(200, 210, 220, 120);
        }}
    """


def back_btn_qss():
    return f"""
        QPushButton {{
            background-color: rgba(40, 60, 84, 200);
            border: 1px solid rgba(140, 180, 220, 80);
            border-radius: 10px;
            color: {qt_theme.c('text')};
            padding: 6px 16px;
            font-size: 12pt;
        }}
        QPushButton:hover {{
            background-color: rgba(60, 90, 120, 230);
            border: 1px solid {qt_theme.c('accent')};
        }}
    """


class GlassCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(card_qss())


class InnerCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("innerCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(inner_card_qss())


class ScrollPage(QScrollArea):
    """Прокручиваемая страница с ЯВНОЙ очисткой фона."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(scroll_qss())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        bg = scroll_bg_color()
        color = QColor(bg)

        # === КЛЮЧ: непрозрачный viewport ===
        vp = self.viewport()
        vp.setAutoFillBackground(True)
        vp.setAttribute(Qt.WA_OpaquePaintEvent, True)
        vp.setAttribute(Qt.WA_TranslucentBackground, False)
        pal = vp.palette()
        pal.setColor(QPalette.Window, color)
        pal.setColor(QPalette.Base, color)
        vp.setPalette(pal)

        # === Внутренний виджет — тоже непрозрачный ===
        self.inner = QWidget()
        self.inner.setAutoFillBackground(True)
        self.inner.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.inner.setAttribute(Qt.WA_TranslucentBackground, False)
        ip = self.inner.palette()
        ip.setColor(QPalette.Window, color)
        ip.setColor(QPalette.Base, color)
        self.inner.setPalette(ip)
        self.setWidget(self.inner)

        s = qt_theme.scale
        self.lay = QVBoxLayout(self.inner)
        self.lay.setContentsMargins(int(6 * s), int(6 * s),
                                     int(12 * s), int(12 * s))
        self.lay.setSpacing(int(12 * s))


class BackButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        s = qt_theme.scale
        self.setFixedSize(int(110 * s), int(40 * s))
        self.setText(f"  {icon('chevron')}   {text}")
        self.setFont(get_icon_font(int(13 * s)))
        self.setStyleSheet(back_btn_qss())


class PageHeader(QWidget):
    """Заголовок с Back-кнопкой."""
    back_clicked = pyqtSignal()

    def __init__(self, title, subtitle="", right_widget=None, parent=None):
        super().__init__(parent)
        from core.i18n import i18n
        s = qt_theme.scale

        # Непрозрачный фон — предотвращает ghosting
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(int(14 * s))

        self.back_btn = BackButton(i18n.t("back_btn"))
        self.back_btn.clicked.connect(self.back_clicked.emit)
        lay.addWidget(self.back_btn)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)

        t_lbl = QLabel(title)
        t_lbl.setFont(qt_theme.font("h2"))
        t_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        text_box.addWidget(t_lbl)

        if subtitle:
            s_lbl = QLabel(subtitle)
            s_lbl.setFont(qt_theme.font("muted"))
            s_lbl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            text_box.addWidget(s_lbl)

        lay.addLayout(text_box)
        lay.addStretch()

        if right_widget:
            lay.addWidget(right_widget)


def answer_option_qss(state="idle"):
    colors = {
        "idle": (f"{qt_theme.c('card')}", "rgba(120, 160, 200, 80)",
                 qt_theme.c("text")),
        "hover": ("rgba(74, 158, 255, 120)", "rgba(140, 190, 240, 200)", "#FFFFFF"),
        "correct": ("rgba(92, 214, 142, 180)", "rgba(140, 235, 180, 230)", "#FFFFFF"),
        "wrong": ("rgba(255, 108, 108, 180)", "rgba(255, 150, 150, 230)", "#FFFFFF"),
        "disabled": ("rgba(40, 60, 84, 150)", "rgba(120, 160, 200, 60)",
                     qt_theme.c("text_muted")),
    }
    bg, border, fg = colors.get(state, colors["idle"])
    return f"""
        QPushButton {{
            background-color: {bg};
            border: 1px solid {border};
            border-radius: 14px;
            color: {fg};
            padding: 16px 22px;
            font-size: 14pt;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: rgba(74, 158, 255, 130);
            border: 1px solid rgba(140, 190, 240, 220);
            color: #FFFFFF;
        }}
        QPushButton:disabled {{ color: {fg}; }}
    """


from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRect


class OpaqueInner(QWidget):
    """
    Внутренний виджет скролла с ЯВНОЙ заливкой фона через paintEvent.
    Обычный QWidget + QSS не всегда чистит старые пиксели.
    """
    def __init__(self, bg_hex: str, parent=None):
        super().__init__(parent)
        self._bg = QColor(bg_hex)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), self._bg)
        p.end()


class OpaqueScrollPage(QScrollArea):
    """
    Скролл-страница, которая ГАРАНТИРОВАННО чистит фон.
    - viewport — непрозрачный
    - inner — кастомный paintEvent
    - без QSS-фонов (только bg цвет)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        bg = scroll_bg_color()
        color = QColor(bg)

        # Viewport — непрозрачный через palette
        vp = self.viewport()
        vp.setAutoFillBackground(True)
        vp.setAttribute(Qt.WA_OpaquePaintEvent, True)
        vp.setAttribute(Qt.WA_TranslucentBackground, False)
        pal = vp.palette()
        pal.setColor(QPalette.Window, color)
        pal.setColor(QPalette.Base, color)
        vp.setPalette(pal)

        # Scrollbars стилизуем
        self.setStyleSheet(scroll_qss())

        # Inner — кастомный opaque-виджет
        self.inner = OpaqueInner(bg)
        self.setWidget(self.inner)

        s = qt_theme.scale
        self.lay = QVBoxLayout(self.inner)
        self.lay.setContentsMargins(int(6 * s), int(6 * s),
                                     int(12 * s), int(12 * s))
        self.lay.setSpacing(int(12 * s))
