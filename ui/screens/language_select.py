# -*- coding: utf-8 -*-
"""Экран выбора языка интерфейса."""
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from core.storage import storage


LANGUAGES = [
    ("ru", "🇷🇺  Русский",   "Russian"),
    ("tk", "🇹🇲  Türkmençe",  "Turkmen"),
    ("en", "🇬🇧  English",   "English"),
]


class LanguageSelectScreen(BaseScreen):

    def _build(self):
        center = tk.Frame(self, bg=theme.c("bg"))
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="中文", font=(theme.cjk_family, 64, "bold"),
                 bg=theme.c("bg"), fg=theme.c("accent")).pack(pady=(0, 8))
        tk.Label(center, text="HSK 5", font=theme.font("h1"),
                 bg=theme.c("bg"), fg=theme.c("text")).pack()

        tk.Label(center, text=self.t("choose_lang_title"),
                 font=theme.font("h3"), bg=theme.c("bg"),
                 fg=theme.c("text_muted")).pack(pady=(28, 18))

        for code, native, _en in LANGUAGES:
            btn = tk.Button(
                center, text=native,
                font=(theme.ui_family, 14), width=22, height=2,
                bg=theme.c("card"), fg=theme.c("text"),
                activebackground=theme.c("accent_soft"),
                relief="flat", bd=0, cursor="hand2",
                highlightbackground=theme.c("border"),
                highlightthickness=1,
                command=lambda c=code: self._pick(c),
            )
            btn.pack(pady=4, ipadx=6, ipady=4)

        tk.Label(center, text=self.t("choose_lang_subtitle"),
                 font=theme.font("muted"), bg=theme.c("bg"),
                 fg=theme.c("text_muted")).pack(pady=(20, 0))

    def _pick(self, code: str):
        storage.set("language", code)
        self.i18n.set_language(code)
        self.manager.show("main_menu", push_history=False)