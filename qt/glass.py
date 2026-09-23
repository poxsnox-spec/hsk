# -*- coding: utf-8 -*-
"""Liquid Glass: фон, QSS. Без QGraphicsEffect — он вызывает ghosting."""
import random
from PyQt5.QtGui import (QPixmap, QPainter, QColor, QLinearGradient,
                         QBrush, QFont, QPen, QFontDatabase)
from PyQt5.QtCore import Qt
from qt.theme import qt_theme

BG_CHARS = "汉字学习研究书道文心画意诗词歌赋"
MATH_CHARS = "xyabf\u03c0\u221a\u221e\u03b8\u03b1\u03b2\u0394"


def _parse_color(s):
    if s.startswith("rgba"):
        p = s[5:-1].split(",")
        return QColor(int(p[0].strip()), int(p[1].strip()),
                      int(p[2].strip()), int(p[3].strip()))
    return QColor(s)


def make_background_pixmap(w, h):
    pm = QPixmap(w, h)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setRenderHint(QPainter.TextAntialiasing, True)

    grad = QLinearGradient(0, 0, 0, h)
    grad.setColorAt(0.0, QColor(qt_theme.c("bg_gradient_top")))
    grad.setColorAt(1.0, QColor(qt_theme.c("bg_gradient_bot")))
    p.fillRect(0, 0, w, h, QBrush(grad))

    random.seed(42)
    pc = _parse_color(qt_theme.c("pattern"))
    s = qt_theme.scale

    for _ in range(28):
        x = random.randint(-50, w + 50)
        y = random.randint(-50, h + 50)
        ch = random.choice(BG_CHARS)
        size = random.randint(int(40 * s), int(130 * s))
        p.setFont(QFont(qt_theme._cjk, size, QFont.Bold))
        p.setPen(QPen(pc))
        p.drawText(x, y, ch)

    for _ in range(20):
        x = random.randint(0, w)
        y = random.randint(0, h)
        ch = random.choice(MATH_CHARS)
        size = random.randint(int(14 * s), int(28 * s))
        p.setFont(QFont("Consolas", size))
        p.setPen(QPen(pc))
        p.drawText(x, y, ch)

    p.end()
    return pm


def soft_shadow(widget, **kwargs):
    """Заглушка — QGraphicsDropShadowEffect вызывает ghosting."""
    return


def card_shadow(widget, **kwargs):
    """Заглушка."""
    return


def liquid_card_qss():
    return f"""
        QFrame#glassCard {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(46, 68, 92, 240),
                stop:0.5 rgba(30, 46, 64, 235),
                stop:1 rgba(18, 28, 42, 230));
            border: 1px solid rgba(120, 160, 200, 70);
            border-top: 1px solid rgba(180, 210, 240, 100);
            border-radius: 18px;
        }}
        QFrame#glassCard:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(60, 88, 120, 240),
                stop:0.5 rgba(40, 62, 88, 235),
                stop:1 rgba(24, 38, 56, 230));
            border: 1px solid rgba(140, 190, 240, 120);
            border-top: 1px solid rgba(200, 230, 255, 160);
        }}
        QFrame#glassCard QLabel {{
            background: transparent;
            color: {qt_theme.c("text")};
        }}
    """


def icon_tile_qss(color: str, border: str, radius: int = 12) -> str:
    return f"""
        QFrame#iconTile {{
            background-color: {color};
            border: 1px solid {border};
            border-radius: {radius}px;
        }}
    """


def sidebar_qss():
    return f"""
        QFrame#sidebar {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(30, 44, 62, 230),
                stop:1 rgba(16, 26, 38, 225));
            border: 1px solid rgba(120, 160, 200, 60);
            border-top: 1px solid rgba(180, 210, 240, 90);
            border-radius: 18px;
        }}
        QPushButton#sideBtn {{
            background-color: transparent;
            border: none;
            border-radius: 12px;
            padding: 14px 18px;
            color: {qt_theme.c("text")};
            font-size: 13pt;
            text-align: left;
        }}
        QPushButton#sideBtn:hover {{
            background-color: rgba(120, 170, 220, 60);
        }}
        QPushButton#sideBtn:pressed {{
            background-color: rgba(60, 90, 120, 110);
        }}
        QFrame#innerCard {{
            background-color: rgba(30, 46, 66, 200);
            border: 1px solid rgba(120, 160, 200, 70);
            border-radius: 12px;
        }}
    """


def continue_card_qss():
    return f"""
        QFrame#continueCard {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(74, 158, 255, 120),
                stop:1 rgba(45, 100, 180, 140));
            border: 1px solid rgba(140, 190, 240, 140);
            border-radius: 14px;
        }}
        QFrame#continueCard:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(100, 180, 255, 150),
                stop:1 rgba(60, 120, 200, 170));
        }}
        QFrame#continueCard QLabel {{ background: transparent; color: #FFFFFF; }}
    """


def streak_card_qss():
    return f"""
        QFrame#streakCard {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 140, 60, 100),
                stop:1 rgba(200, 90, 40, 120));
            border: 1px solid rgba(255, 180, 100, 130);
            border-radius: 14px;
        }}
        QFrame#streakCard QLabel {{ background: transparent; color: #FFFFFF; }}
    """


def opaque_card_qss():
    """
    НЕпрозрачная карточка для скролл-экранов.
    Полупрозрачные QSS + QScrollArea = ghosting при скролле.
    """
    return """
        QFrame#glassCard {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2E445C,
                stop:0.5 #1E2E40,
                stop:1 #121C2A);
            border: 1px solid #3A5068;
            border-top: 1px solid #506E8C;
            border-radius: 18px;
        }
        QFrame#glassCard:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3C5878,
                stop:0.5 #283E58,
                stop:1 #182638);
            border: 1px solid #5A80A0;
            border-top: 1px solid #6E96B8;
        }
        QFrame#glassCard QLabel {
            background: transparent;
            color: #F0F4F8;
        }
    """


def opaque_icon_tile_qss(color_hex: str, border_hex: str, radius: int = 12) -> str:
    """НЕпрозрачная плитка под иконку."""
    return f"""
        QFrame#iconTile {{
            background-color: {color_hex};
            border: 1px solid {border_hex};
            border-radius: {radius}px;
        }}
    """
