# -*- coding: utf-8 -*-
"""Главное меню — стеклянный стиль."""
import random
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from core.config import APP_NAME, APP_VERSION
from core.storage import storage
from core.glass import rounded_rect, BG_CHARS, MATH_CHARS


# Пункты меню: (ключ, target, эмодзи)
MENU_ITEMS = [
    ("menu_lessons",   "lessons",  "📚"),
    ("menu_vocab",     "vocab",    "📓"),
    ("menu_srs",       "srs",      "🔁"),
    ("menu_heatmap",   "heatmap",  "📊"),
    ("menu_stats",     "stats",    "📈"),
    ("analyzer_title", "analyzer", "🔍"),
]

SIDE_ITEMS = [
    ("change_lang",  "lang",     "🌐"),
    ("__theme__",    "theme",    "☀"),
    ("menu_settings","settings", "⚙"),
    ("menu_about",   "about",    "ℹ"),
]


class MainMenuScreen(BaseScreen):

    def _build(self):
        self.canvas = tk.Canvas(
            self, bg=theme.c("bg"), highlightthickness=0, bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self._card_hover_id = None
        self._card_rects = {}     # tag -> rect_id
        self._card_tags = {}      # rect_id -> tag

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Button-1>", self._on_click)

    # ============================================================
    #                 Рендер всего экрана
    # ============================================================
    def _on_resize(self, event):
        w, h = event.width, event.height
        if w < 200 or h < 200:
            return
        self.canvas.delete("all")
        self._draw_background(w, h)
        self._draw_header(w, h)
        self._draw_cards(w, h)
        self._draw_sidebar(w, h)

    # ------------------------------------------------------------
    def _draw_background(self, w, h):
        """Тёмный фон с россыпью иероглифов и математических символов."""
        # Сплошной фон
        self.canvas.create_rectangle(0, 0, w, h,
                                     fill=theme.c("bg"), outline="")

        random.seed(42)  # стабильный паттерн при каждом запуске
        pattern = theme.c("pattern")

        # Крупные иероглифы — фон
        for _ in range(28):
            x = random.randint(-40, w + 40)
            y = random.randint(-40, h + 40)
            ch = random.choice(BG_CHARS)
            size = random.randint(int(40 * theme.scale), int(120 * theme.scale))
            self.canvas.create_text(x, y, text=ch, fill=pattern,
                                    font=(theme.cjk_family, size, "bold"))

        # Маленькие математические символы
        for _ in range(20):
            x = random.randint(0, w)
            y = random.randint(0, h)
            ch = random.choice(MATH_CHARS)
            size = random.randint(int(14 * theme.scale), int(28 * theme.scale))
            self.canvas.create_text(x, y, text=ch, fill=pattern,
                                    font=("Consolas", size))

    # ------------------------------------------------------------
    def _draw_header(self, w, h):
        s = theme.scale
        pad = int(40 * s)

        # Логотип
        self.canvas.create_text(
            pad, int(50 * s), text="中文", anchor="w",
            fill=theme.c("text"), font=theme.font("glass_logo"),
        )
        self.canvas.create_text(
            pad + int(90 * s), int(50 * s), text="· " + APP_NAME, anchor="w",
            fill=theme.c("text"), font=theme.font("glass_header"),
        )
        self.canvas.create_text(
            pad, int(85 * s), text=f"v{APP_VERSION}", anchor="w",
            fill=theme.c("text_muted"), font=theme.font("muted"),
        )

    # ------------------------------------------------------------
    def _draw_cards(self, w, h):
        s = theme.scale
        pad_l = int(40 * s)
        sidebar_w = int(300 * s)
        card_w = w - pad_l * 2 - sidebar_w - int(24 * s)

        card_h = int(66 * s)
        gap = int(12 * s)
        y0 = int(120 * s)

        for i, (key, target, icon) in enumerate(MENU_ITEMS):
            y = y0 + i * (card_h + gap)
            self._make_card(
                x1=pad_l, y1=y, x2=pad_l + card_w, y2=y + card_h,
                label=self.t(key), icon=icon,
                tag=f"card_{key}",
                command=lambda t=target: self._open(t),
            )

    # ------------------------------------------------------------
    def _make_card(self, x1, y1, x2, y2, label, icon, tag, command):
        """Создаёт стеклянную карточку и запоминает её."""
        # Основной прямоугольник
        rect = rounded_rect(
            self.canvas, x1, y1, x2, y2, r=int(16 * theme.scale),
            fill=theme.c("card"),
            outline=theme.c("glass_border"),
            width=1,
        )
        # Текст слева
        self.canvas.create_text(
            x1 + int(24 * theme.scale), (y1 + y2) // 2,
            text=label, anchor="w",
            fill=theme.c("text"),
            font=theme.font("glass_card"),
            tags=(tag,),
        )
        # Иконка справа
        self.canvas.create_text(
            x2 - int(24 * theme.scale), (y1 + y2) // 2,
            text=icon, anchor="e",
            fill=theme.c("text"),
            font=theme.font("glass_icon"),
            tags=(tag,),
        )

        # Все элементы одной карточки — в одну группу по тегу
        self.canvas.itemconfig(rect, tags=(tag,))
        # Rect храним отдельно, чтобы потом перекрашивать
        self._card_rects[tag] = rect
        # Обратный индекс: rect_id -> tag
        self._card_tags[rect] = tag
        # Ассоциируем действие с тегом
        self.canvas.tag_bind(tag, "<Button-1>",
                             lambda _e, c=command: c())

    # ------------------------------------------------------------
    def _draw_sidebar(self, w, h):
        s = theme.scale
        sidebar_w = int(300 * s)
        pad = int(40 * s)
        x1 = w - sidebar_w - pad
        x2 = w - pad
        y1 = int(120 * s)

        # Стеклянная панель
        panel_h = int(len(SIDE_ITEMS) * 62 * s + 20 * s)
        rounded_rect(
            self.canvas, x1, y1, x2, y1 + panel_h, r=int(16 * s),
            fill=theme.c("glass_sidebar"),
            outline=theme.c("glass_border"),
            width=1,
        )

        # Пункты сайдбара
        for i, (key, action, icon) in enumerate(SIDE_ITEMS):
            yy = y1 + int(10 * s) + i * int(62 * s)
            if key == "__theme__":
                # Надпись, показывающая на что переключится
                if theme.mode == "glass":
                    label = self.t("theme_light")
                elif theme.mode == "dark":
                    label = self.t("theme_light")
                else:
                    label = self.t("theme_dark")
            else:
                label = self.t(key)

            tag = f"side_{action}"
            rect = rounded_rect(
                self.canvas, x1 + int(10 * s), yy,
                x2 - int(10 * s), yy + int(50 * s), r=int(10 * s),
                fill=theme.c("glass_sidebar"),
                outline="",
            )
            self.canvas.itemconfig(rect, tags=(tag,))
            self._card_rects[tag] = rect
            self._card_tags[rect] = tag

            # Текст
            self.canvas.create_text(
                x1 + int(30 * s), yy + int(25 * s),
                text=label, anchor="w",
                fill=theme.c("text"),
                font=theme.font("glass_side"),
                tags=(tag,),
            )
            # Иконка
            self.canvas.create_text(
                x2 - int(28 * s), yy + int(25 * s),
                text=icon, anchor="e",
                fill=theme.c("text"),
                font=theme.font("glass_side"),
                tags=(tag,),
            )
            self.canvas.tag_bind(tag, "<Button-1>",
                                 lambda _e, a=action: self._side_action(a))

    # ============================================================
    #                Hover-эффект
    # ============================================================
    def _on_motion(self, event):
        item_ids = self.canvas.find_overlapping(
            event.x - 1, event.y - 1, event.x + 1, event.y + 1,
        )
        new_hover = None
        for iid in reversed(item_ids):
            if iid in self._card_tags:
                new_hover = self._card_tags[iid]
                break

        if new_hover == self._card_hover_id:
            return

        # Снимаем hover со старой
        if self._card_hover_id:
            old_rect = self._card_rects.get(self._card_hover_id)
            if old_rect:
                self.canvas.itemconfig(old_rect, fill=theme.c("card")
                                       if not self._card_hover_id.startswith("side_")
                                       else theme.c("glass_sidebar"))

        # Ставим на новую
        if new_hover:
            new_rect = self._card_rects.get(new_hover)
            if new_rect:
                self.canvas.itemconfig(new_rect,
                                       fill=theme.c("card_hover"))
        self._card_hover_id = new_hover

    # ============================================================
    def _on_click(self, event):
        """Canvas-level клики не нужны — всё через tag_bind."""
        pass

    # ============================================================
    #                Действия
    # ============================================================
    def _open(self, target):
        if target == "analyzer":
            self.manager.show("analyzer", unit=1, index=1)
        elif target:
            self.manager.show(target)

    def _side_action(self, action):
        if action == "lang":
            self.manager.show("language_select")
        elif action == "theme":
            theme.toggle()
            storage.set("theme_mode", theme.mode)
            self.manager.show("main_menu", push_history=False)
        elif action == "about":
            self._show_about()
        # settings — заглушка

    def _show_about(self):
        from tkinter import messagebox
        messagebox.showinfo(
            "About",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Тренажёр по учебнику HSK 5 上.\n"
            "Учебник: 姜丽萍 (ed.), 北京语言大学出版社, 2015.",
        )
