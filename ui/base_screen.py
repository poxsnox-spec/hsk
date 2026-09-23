# -*- coding: utf-8 -*-
"""Базовый класс всех экранов."""
import tkinter as tk
from core.theme import theme
from core.i18n import i18n


class BaseScreen(tk.Frame):
    """Каждый экран наследуется от этого класса."""

    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, bg=theme.c("bg"))
        self.manager = manager
        self.i18n = i18n
        self.theme = theme
        self._kwargs = kwargs
        self._build()

    def _build(self):
        """Переопределяется в потомках — здесь строится UI."""
        raise NotImplementedError

    # ---- Утилиты ----
    def t(self, key: str) -> str:
        return self.i18n.t(key)

    def make_header(self, title: str, back_to=None) -> tk.Frame:
        """Строит единый заголовок для всех экранов."""
        bar = tk.Frame(self, bg=theme.c("bg"))
        bar.pack(fill="x", padx=24, pady=(18, 8))

        if back_to is not None:
            btn = tk.Button(
                bar, text=self.t("back"),
                font=theme.font("body"), bg=theme.c("bg"),
                fg=theme.c("accent_dark"), activebackground=theme.c("bg_soft"),
                relief="flat", cursor="hand2",
                command=lambda: self.manager.show(back_to),
            )
            btn.pack(side="left")

        lbl = tk.Label(bar, text=title, font=theme.font("h2"),
                       bg=theme.c("bg"), fg=theme.c("text"))
        lbl.pack(side="left", padx=12)
        return bar

    def make_card(self, parent=None, **pack_kwargs) -> tk.Frame:
        """Карточка — белый блок с рамкой."""
        parent = parent or self
        card = tk.Frame(parent, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(**pack_kwargs)
        return card