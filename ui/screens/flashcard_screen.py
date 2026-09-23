# -*- coding: utf-8 -*-
"""Режим флеш-карточек с переворотом."""
import random
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from models.lesson import load_lesson
from core.audio import audio
from core.storage import storage


class FlashcardScreen(BaseScreen):
    def _build(self):
        self.unit = self._kwargs.get("unit", 1)
        self.index = self._kwargs.get("index", 1)
        self.lesson = load_lesson(self.unit, self.index)

        self.cards = self.lesson.vocabulary[:]
        random.shuffle(self.cards)
        self.pos = 0
        self.flipped = False

        self.make_header(self.t("flashcards"), back_to="lesson_view")

        self.counter = tk.Label(self, text="", font=theme.font("body"),
                                bg=theme.c("bg"), fg=theme.c("text_muted"))
        self.counter.pack(pady=(0, 6))

        self.card = tk.Frame(self, bg=theme.c("card"),
                             highlightbackground=theme.c("border"),
                             highlightthickness=2, cursor="hand2")
        self.card.pack(padx=60, pady=20, fill="both", expand=True)

        self.hanzi = tk.Label(self.card, text="", font=(theme.cjk_family, 100, "bold"),
                              bg=theme.c("card"), fg=theme.c("text"))
        self.hanzi.pack(pady=(60, 10))
        self.pinyin = tk.Label(self.card, text="", font=theme.font("pinyin"),
                               bg=theme.c("card"), fg=theme.c("accent"))
        self.pinyin.pack()
        self.translation = tk.Label(self.card, text="", font=theme.font("h3"),
                                    bg=theme.c("card"), fg=theme.c("text_muted"))
        self.translation.pack(pady=10)
        tk.Label(self.card, text=self.t("fc_hint"),
                 font=theme.font("muted"), bg=theme.c("card"),
                 fg=theme.c("text_muted")).pack(side="bottom", pady=10)

        for w in (self.card, self.hanzi, self.pinyin, self.translation):
            w.bind("<Button-1>", lambda _e: self._flip())
        self.bind_all("<space>", lambda _e: self._flip())
        self.bind_all("<Right>", lambda _e: self._next())

        ctrl = tk.Frame(self, bg=theme.c("bg"))
        ctrl.pack(pady=14)
        tk.Button(ctrl, text="◀", font=(theme.ui_family, 16),
                  bg=theme.c("bg"), relief="flat", padx=16,
                  cursor="hand2", command=lambda: self._move(-1)).pack(side="left")
        tk.Button(ctrl, text="🔊", font=(theme.ui_family, 16),
                  bg=theme.c("bg"), relief="flat", padx=16,
                  cursor="hand2", command=self._play).pack(side="left", padx=8)
        tk.Button(ctrl, text="▶", font=(theme.ui_family, 16),
                  bg=theme.c("bg"), relief="flat", padx=16,
                  cursor="hand2", command=lambda: self._move(1)).pack(side="left")

        self._render()

    def _render(self):
        w = self.cards[self.pos]
        self.counter.config(text=f"{self.pos + 1} / {len(self.cards)}")
        self.hanzi.config(text=w.hanzi)
        if self.flipped:
            self.pinyin.config(text=w.pinyin)
            self.translation.config(text=w.translate(self.i18n.language))
        else:
            self.pinyin.config(text="?")
            self.translation.config(text="")

    def _flip(self):
        self.flipped = not self.flipped
        if self.flipped:
            storage.record_word(self.cards[self.pos].hanzi, correct=True)
        self._render()

    def _move(self, d):
        self.flipped = False
        self.pos = (self.pos + d) % len(self.cards)
        self._render()

    def _next(self):
        self._move(1)

    def _play(self):
        w = self.cards[self.pos]
        if w.audio and audio.exists(self.unit, self.index, w.audio):
            audio.play(audio.find(self.unit, self.index, w.audio))