# -*- coding: utf-8 -*-
"""Тренажёр: 3 режима — hanzi→перевод, перевод→hanzi, пиньинь→hanzi."""
import random
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from models.lesson import load_lesson
from core.storage import storage


class TrainerScreen(BaseScreen):
    def _build(self):
        self.unit = self._kwargs.get("unit", 1)
        self.index = self._kwargs.get("index", 1)
        self.lesson = load_lesson(self.unit, self.index)

        self.make_header("🎯 " + self.t("menu_trainer"), back_to="main_menu")

        self.mode_bar = tk.Frame(self, bg=theme.c("bg"))
        self.mode_bar.pack(fill="x", padx=28, pady=(4, 8))
        self.modes = [
            ("hanzi_to_tr", self.t("quiz_hanzi_to_translation")),
            ("tr_to_hanzi", self.t("quiz_translation_to_hanzi")),
            ("pinyin_to_hanzi", self.t("quiz_pinyin_to_hanzi")),
        ]
        self.mode_btns = {}
        for key, label in self.modes:
            btn = tk.Button(self.mode_bar, text=label, font=theme.font("body"),
                            bg=theme.c("bg"), fg=theme.c("text_muted"),
                            activebackground=theme.c("accent_soft"),
                            relief="flat", padx=12, pady=8, cursor="hand2",
                            command=lambda k=key: self._set_mode(k))
            btn.pack(side="left", padx=4)
            self.mode_btns[key] = btn

        self.score = 0
        self.total = 0
        self.streak = 0
        self.locked = False

        self.top = tk.Label(self, text="", font=theme.font("body"),
                            bg=theme.c("bg"), fg=theme.c("text_muted"))
        self.top.pack(pady=(0, 6))
        self.question_lbl = tk.Label(self, text="", font=(theme.cjk_family, 64, "bold"),
                                     bg=theme.c("bg"), fg=theme.c("accent"))
        self.question_lbl.pack(pady=(0, 6))
        self.sub_lbl = tk.Label(self, text="", font=theme.font("pinyin"),
                                bg=theme.c("bg"), fg=theme.c("text_muted"))
        self.sub_lbl.pack(pady=(0, 12))
        self.opts_frame = tk.Frame(self, bg=theme.c("bg"))
        self.opts_frame.pack(pady=6)
        self.feedback = tk.Label(self, text="", font=theme.font("h3"),
                                 bg=theme.c("bg"), fg=theme.c("text"))
        self.feedback.pack(pady=8)
        self._set_mode("hanzi_to_tr")

    def _set_mode(self, key):
        self.mode = key
        self.score = 0
        self.total = 0
        self.streak = 0
        for k, btn in self.mode_btns.items():
            active = (k == key)
            btn.configure(bg=theme.c("accent") if active else theme.c("bg"),
                          fg="white" if active else theme.c("text_muted"))
        self._next_question()

    def _next_question(self):
        for ch in self.opts_frame.winfo_children():
            ch.destroy()
        self.feedback.config(text="")
        self.locked = False

        word = random.choice(self.lesson.vocabulary)
        self.correct = word
        pool = [w for w in self.lesson.vocabulary if w.hanzi != word.hanzi]
        wrong = random.sample(pool, min(3, len(pool)))
        options = [word] + wrong
        random.shuffle(options)

        if self.mode == "hanzi_to_tr":
            self.question_lbl.config(text=word.hanzi, font=theme.font("hanzi_l"))
            self.sub_lbl.config(text=word.pinyin)
            btn_text = lambda w: w.translate(self.i18n.language)
        elif self.mode == "tr_to_hanzi":
            self.question_lbl.config(text=word.translate(self.i18n.language),
                                     font=(theme.ui_family, 26, "bold"))
            self.sub_lbl.config(text="")
            btn_text = lambda w: w.hanzi
        else:
            self.question_lbl.config(text=word.pinyin,
                                     font=(theme.ui_family, 32, "bold"))
            self.sub_lbl.config(text="")
            btn_text = lambda w: w.hanzi

        self.top.config(text=f"{self.t('score')}: {self.score} / {self.total}   "
                             f"🔥 {self.streak}")

        for i, opt in enumerate(options):
            btn = tk.Button(self.opts_frame, text=btn_text(opt),
                            font=(theme.cjk_family, 16),
                            bg=theme.c("card"), fg=theme.c("text"),
                            activebackground=theme.c("accent_soft"),
                            relief="flat", width=22, pady=10,
                            cursor="hand2",
                            command=lambda o=opt: self._check(o))
            btn.grid(row=i // 2, column=i % 2, padx=6, pady=4)

    def _check(self, chosen):
        if self.locked:
            return
        self.locked = True
        self.total += 1
        correct = (chosen.hanzi == self.correct.hanzi)
        if correct:
            self.score += 1
            self.streak += 1
            self.feedback.config(text="✓ " + self.t("correct"), fg=theme.c("success"))
        else:
            self.streak = 0
            self.feedback.config(
                text=f"✗ {self.t('wrong')}.  {self.t('correct_answer')}: "
                     f"{self.correct.hanzi} ({self.correct.pinyin})",
                fg=theme.c("error"))
        storage.record_word(self.correct.hanzi, correct)
        self.after(900, self._next_question)