# -*- coding: utf-8 -*-
"""Экран упражнений рабочей тетради: 听力 / 阅读."""
import tkinter as tk
from ui.base_screen import BaseScreen
from ui.widgets.scrollable import ScrollableFrame
from core.theme import theme
from core.audio import audio
from models.lesson import load_lesson
from core.storage import storage


class ExerciseScreen(BaseScreen):
    def _build(self):
        self.unit = self._kwargs.get("unit", 1)
        self.index = self._kwargs.get("index", 1)
        self.mode = self._kwargs.get("mode", "reading")
        self.lesson = load_lesson(self.unit, self.index)

        questions = (self.lesson.wb_listening if self.mode == "listening"
                     else self.lesson.wb_reading)

        title = self.t("wb_listening") if self.mode == "listening" else self.t("wb_reading")
        self.make_header(title, back_to="lesson_view")

        self.score = 0
        self.answered = 0
        self.q_index = 0
        self.questions = questions
        self.locked = False

        self.top = tk.Label(self, text="", font=theme.font("body"),
                            bg=theme.c("bg"), fg=theme.c("text_muted"))
        self.top.pack(pady=(0, 8))

        if self.mode == "listening":
            ctrl = tk.Frame(self, bg=theme.c("bg"))
            ctrl.pack()
            for key in ("workbook_01_1", "workbook_01_2"):
                fname = self.lesson.audio_files.get(key, "")
                has = fname and audio.exists(self.unit, self.index, fname)
                tk.Button(ctrl, text=f"🔊 {key}",
                          font=theme.font("body"),
                          bg=theme.c("card") if has else theme.c("bg_soft"),
                          fg=theme.c("accent") if has else theme.c("text_muted"),
                          relief="flat", padx=12, pady=6,
                          state="normal" if has else "disabled",
                          cursor="hand2" if has else "",
                          command=(lambda f=fname: audio.play(
                              audio.find(self.unit, self.index, f))) if has else None,
                          ).pack(side="left", padx=4)

        self.sf = ScrollableFrame(self)
        self.sf.pack(fill="both", expand=True, padx=24, pady=(12, 16))
        self._render_question()

    def _render_question(self):
        for ch in self.sf.inner.winfo_children():
            ch.destroy()
        if self.q_index >= len(self.questions):
            self._render_finish()
            return
        q = self.questions[self.q_index]
        self.locked = False
        self.top.config(text=f"{self.q_index + 1} / {len(self.questions)}   "
                             f"{self.t('score')}: {self.score}")

        prompt = q.prompt.get(self.i18n.language) or q.prompt.get("en", "")
        box = tk.Frame(self.sf.inner, bg=theme.c("card"),
                       highlightbackground=theme.c("border"),
                       highlightthickness=1)
        box.pack(fill="x", pady=6)
        tk.Label(box, text=f"№ {self.q_index + 1}",
                 font=theme.font("muted"), bg=theme.c("card"),
                 fg=theme.c("accent"), anchor="w", padx=16, pady=10).pack(fill="x")
        tk.Label(box, text=prompt, font=(theme.cjk_family, 14),
                 bg=theme.c("card"), fg=theme.c("text"),
                 wraplength=880, justify="left", anchor="w",
                 padx=16, pady=4).pack(fill="x")

        self.opt_buttons = []
        self.feedback = tk.Label(self.sf.inner, text="", font=theme.font("h3"),
                                 bg=theme.c("bg"), fg=theme.c("text"))
        for i, opt in enumerate(q.options):
            letter = "ABCD"[i]
            btn = tk.Button(self.sf.inner, text=f"{letter}. {opt}",
                            font=(theme.cjk_family, 13),
                            bg=theme.c("card"), fg=theme.c("text"),
                            activebackground=theme.c("accent_soft"),
                            relief="flat", anchor="w", padx=16, pady=10,
                            cursor="hand2",
                            command=lambda idx=i: self._check(idx))
            btn.pack(fill="x", pady=3)
            self.opt_buttons.append(btn)
        self.feedback.pack(fill="x", pady=8)

    def _check(self, idx):
        if self.locked:
            return
        self.locked = True
        q = self.questions[self.q_index]
        correct = (idx == q.answer)
        self.answered += 1
        if correct:
            self.score += 1
        for i, btn in enumerate(self.opt_buttons):
            if i == q.answer:
                btn.configure(bg=theme.c("success_bg"), fg=theme.c("success"))
            elif i == idx and not correct:
                btn.configure(bg=theme.c("error_bg"), fg=theme.c("error"))
        if correct:
            self.feedback.config(text="✓ " + self.t("correct"), fg=theme.c("success"))
        else:
            right = q.options[q.answer]
            self.feedback.config(
                text=f"✗ {self.t('wrong')}.  {self.t('correct_answer')}: {right}",
                fg=theme.c("error"))
        self.sf.inner.after(1200, self._next)

    def _next(self):
        self.q_index += 1
        self._render_question()

    def _render_finish(self):
        for ch in self.sf.inner.winfo_children():
            ch.destroy()
        storage.update_score(f"{self.lesson.lesson_id}_{self.mode}",
                             self.score, len(self.questions))
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=30)
        tk.Label(card, text="🎉 " + self.t("quiz_session_end"),
                 font=theme.font("h2"), bg=theme.c("card"),
                 fg=theme.c("accent"), pady=20).pack()
        tk.Label(card, text=f"{self.score} / {len(self.questions)}",
                 font=(theme.ui_family, 28, "bold"),
                 bg=theme.c("card"), fg=theme.c("text")).pack()
        tk.Label(card, text=self.t("score"), font=theme.font("body"),
                 bg=theme.c("card"), fg=theme.c("text_muted"),
                 pady=20).pack()
        btns = tk.Frame(self.sf.inner, bg=theme.c("bg"))
        btns.pack()
        tk.Button(btns, text=self.t("quiz_again"), font=theme.font("body"),
                  bg=theme.c("accent"), fg="white", relief="flat",
                  padx=16, pady=8, cursor="hand2",
                  command=self._restart).pack(side="left", padx=6)
        tk.Button(btns, text=self.t("back"), font=theme.font("body"),
                  bg=theme.c("card"), fg=theme.c("text"), relief="flat",
                  padx=16, pady=8, cursor="hand2",
                  command=lambda: self.manager.show("lesson_view",
                                                     unit=self.unit, index=self.index),
                  ).pack(side="left", padx=6)

    def _restart(self):
        self.score = 0
        self.answered = 0
        self.q_index = 0
        self._render_question()