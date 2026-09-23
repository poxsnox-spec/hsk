
# -*- coding: utf-8 -*-
"""Тема для PyQt5: glass + light + dark."""
from PyQt5.QtGui import QFont

GLASS = {
    "bg": "#0A1018", "bg_gradient_top": "#0D1724", "bg_gradient_bot": "#060B12",
    "card": "rgba(24, 37, 51, 200)", "card_hover": "rgba(34, 56, 78, 220)",
    "card_pressed": "rgba(18, 28, 42, 240)",
    "card_border": "rgba(58, 80, 104, 255)",
    "card_border_hover": "#66B2FF",
    "sidebar": "rgba(16, 27, 40, 200)",
    "sidebar_border": "rgba(58, 80, 104, 180)",
    "text": "#F0F4F8", "text_muted": "#8B9AAB",
    "accent": "#66B2FF", "accent_dark": "#4A8FCC",
    "accent_soft": "rgba(26, 58, 92, 180)",
    "success": "#5CD68E", "error": "#FF6B6B", "warn": "#FFB84D",
    "pattern": "rgba(80, 120, 160, 30)",
}
LIGHT = {
    "bg": "#FAF7F0", "bg_gradient_top": "#FFFFFF", "bg_gradient_bot": "#F2EDE3",
    "card": "rgba(255, 255, 255, 240)", "card_hover": "rgba(245, 240, 228, 250)",
    "card_pressed": "rgba(230, 222, 205, 255)",
    "card_border": "rgba(228, 219, 200, 255)",
    "card_border_hover": "#B03A2E",
    "sidebar": "rgba(250, 247, 240, 240)",
    "sidebar_border": "rgba(228, 219, 200, 255)",
    "text": "#2B2B2B", "text_muted": "#7A7166",
    "accent": "#B03A2E", "accent_dark": "#8B2E24",
    "accent_soft": "rgba(245, 218, 214, 200)",
    "success": "#2E7D32", "error": "#C62828", "warn": "#EF6C00",
    "pattern": "rgba(180, 150, 100, 40)",
}
DARK = {
    "bg": "#1A1A1A", "bg_gradient_top": "#1E1E1E", "bg_gradient_bot": "#141414",
    "card": "rgba(46, 46, 46, 220)", "card_hover": "rgba(60, 60, 60, 240)",
    "card_pressed": "rgba(38, 38, 38, 255)",
    "card_border": "rgba(64, 64, 64, 255)", "card_border_hover": "#EF6B5E",
    "sidebar": "rgba(35, 35, 35, 220)",
    "sidebar_border": "rgba(70, 70, 70, 200)",
    "text": "#E8E8E8", "text_muted": "#A0A0A0",
    "accent": "#EF6B5E", "accent_dark": "#C13A31",
    "accent_soft": "rgba(61, 36, 32, 180)",
    "success": "#66BB6A", "error": "#EF5350", "warn": "#FFB74D",
    "pattern": "rgba(120, 120, 120, 40)",
}


class QtTheme:
    def __init__(self):
        self._mode = "glass"
        self._cjk = "Microsoft YaHei UI"
        self._ui = "Segoe UI"
        self._scale = 1.0
        self.fonts = {}

    def init(self, cjk_family=None, ui_family=None, dpi_scale=1.0):
        if cjk_family: self._cjk = cjk_family
        if ui_family: self._ui = ui_family
        self._scale = max(1.0, min(dpi_scale, 2.5))
        def px(b): return max(8, int(round(b * self._scale)))
        self.fonts = {
            "h1": QFont(self._ui, px(26), QFont.Bold),
            "h2": QFont(self._ui, px(20), QFont.Bold),
            "h3": QFont(self._ui, px(15), QFont.Bold),
            "body": QFont(self._ui, px(12)),
            "body_bold": QFont(self._ui, px(12), QFont.Bold),
            "muted": QFont(self._ui, px(10)),
            "card": QFont(self._ui, px(18), QFont.Bold),
            "side": QFont(self._ui, px(14)),
            "logo": QFont(self._cjk, px(42), QFont.Bold),
            "icon": QFont("Segoe UI Emoji", px(24)),
        }

    @property
    def mode(self): return self._mode
    @property
    def scale(self): return self._scale

    def set_mode(self, mode):
        self._mode = mode if mode in ("glass", "light", "dark") else "glass"

    def toggle(self):
        order = ["glass", "dark", "light"]
        i = order.index(self._mode)
        self._mode = order[(i + 1) % len(order)]
        return self._mode

    def c(self, key):
        return {"glass": GLASS, "dark": DARK, "light": LIGHT}[self._mode].get(key, "#000")

    def font(self, key):
        return self.fonts.get(key, self.fonts["body"])


qt_theme = QtTheme()
