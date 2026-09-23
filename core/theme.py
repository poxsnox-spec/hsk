# -*- coding: utf-8 -*-
"""Тема: light / dark / glass палитры + шрифты с авто-масштабом."""
import tkinter.font as tkfont


LIGHT_COLORS = {
    "bg": "#FAF7F0", "bg_soft": "#F2EDE3", "card": "#FFFFFF",
    "card_hover": "#F5EFE3", "border": "#E4DBC8",
    "text": "#2B2B2B", "text_muted": "#7A7166",
    "accent": "#B03A2E", "accent_dark": "#8B2E24", "accent_soft": "#F5DAD6",
    "success": "#2E7D32", "success_bg": "#E3F0E4",
    "error": "#C62828", "error_bg": "#F8DDDD",
    "warn": "#EF6C00", "gold": "#C9A227",
    "info_bg": "#EAF2FA", "info": "#1565C0",
    "pattern": "#E8DFCD",
    "glass_border": "#D4C9B3",
    "glass_sidebar": "#F4EEDF",
}

DARK_COLORS = {
    "bg": "#1A1A1A", "bg_soft": "#262626", "card": "#2E2E2E",
    "card_hover": "#383838", "border": "#404040",
    "text": "#E8E8E8", "text_muted": "#A0A0A0",
    "accent": "#EF6B5E", "accent_dark": "#C13A31", "accent_soft": "#3D2420",
    "success": "#66BB6A", "success_bg": "#1E3A22",
    "error": "#EF5350", "error_bg": "#3D1F1F",
    "warn": "#FFB74D", "gold": "#D4AF37",
    "info_bg": "#1A2A3A", "info": "#64B5F6",
    "pattern": "#252525",
    "glass_border": "#4A4A4A",
    "glass_sidebar": "#232323",
}

# Стеклянная палитра — как на скрине (тёмный синий)
GLASS_COLORS = {
    "bg":            "#0A1018",
    "bg_soft":       "#131C26",
    "card":          "#182533",
    "card_hover":    "#22384E",
    "border":        "#2E455C",
    "text":          "#F0F4F8",
    "text_muted":    "#8B9AAB",
    "accent":        "#66B2FF",
    "accent_dark":   "#4A8FCC",
    "accent_soft":   "#1A3A5C",
    "success":       "#5CD68E",
    "success_bg":    "#153826",
    "error":         "#FF6B6B",
    "error_bg":      "#3A1A1A",
    "warn":          "#FFB84D",
    "gold":          "#E0C158",
    "info_bg":       "#132A42",
    "info":          "#7EB8FF",
    "pattern":       "#111C28",
    "glass_border":  "#3A5068",
    "glass_sidebar": "#101B28",
}

COLORS = LIGHT_COLORS

_CJK_CANDIDATES = [
    "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "SimSun",
    "Noto Sans CJK SC", "PingFang SC", "Source Han Sans SC",
    "WenQuanYi Micro Hei", "Arial Unicode MS",
]
_UI_CANDIDATES = ["Segoe UI", "Helvetica Neue", "Arial", "TkDefaultFont"]


def _pick_font(candidates):
    try:
        available = set(tkfont.families())
    except Exception:
        return candidates[-1]
    for f in candidates:
        if f in available:
            return f
    return candidates[-1]


class Theme:
    def __init__(self):
        self._initialized = False
        self._mode = "glass"
        self._scale = 1.0

    def init(self, dpi_scale=None):
        if self._initialized:
            return
        dpi_scale = 1.0 if dpi_scale is None else dpi_scale
        self._scale = max(1.0, min(dpi_scale, 2.5))

        cjk = _pick_font(_CJK_CANDIDATES)
        ui = _pick_font(_UI_CANDIDATES)
        self.cjk_family = cjk
        self.ui_family = ui
        s = self._scale

        def px(b):
            return max(8, int(round(b * s)))

        self.fonts = {
            "h1": (ui, px(26), "bold"),
            "h2": (ui, px(20), "bold"),
            "h3": (ui, px(15), "bold"),
            "h4": (ui, px(14), "bold"),
            "body": (ui, px(12)),
            "body_bold": (ui, px(12), "bold"),
            "muted": (ui, px(10)),
            "hanzi_xl": (cjk, px(88), "bold"),
            "hanzi_l": (cjk, px(56), "bold"),
            "hanzi_m": (cjk, px(32), "bold"),
            "hanzi_s": (cjk, px(22), "bold"),
            "hanzi_xs": (cjk, px(16)),
            "pinyin": ("Arial", px(16)),
            "pinyin_s": ("Arial", px(12)),
            "glass_header": (ui, px(30), "bold"),
            "glass_card": (ui, px(18), "bold"),
            "glass_side": (ui, px(14)),
            "glass_icon": ("Segoe UI Emoji", px(26)),
            "glass_logo": (cjk, px(42), "bold"),
        }
        self._initialized = True

    @property
    def mode(self):
        return self._mode

    @property
    def scale(self):
        return self._scale

    def set_mode(self, mode):
        if mode in ("light", "dark", "glass"):
            self._mode = mode
        else:
            self._mode = "glass"

    def toggle(self):
        order = ["glass", "dark", "light"]
        i = order.index(self._mode)
        self._mode = order[(i + 1) % len(order)]
        return self._mode

    def font(self, key):
        return self.fonts.get(key, self.fonts["body"])

    def palette(self):
        if self._mode == "glass":
            return GLASS_COLORS
        if self._mode == "dark":
            return DARK_COLORS
        return LIGHT_COLORS

    def c(self, key):
        return self.palette().get(key, "#000000")


theme = Theme()
