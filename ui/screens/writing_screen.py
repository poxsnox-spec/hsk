# -*- coding: utf-8 -*-
"""Экран письма: перестановка предложений + эссе."""
import random
import tkinter as tk
from ui.base_screen import BaseScreen
from ui.widgets.scrollable import ScrollableFrame
from core.theme import theme
from models.lesson import load_lesson


class WritingScreen(BaseScreen):
    def _build(self):
        self.unit = self._kwargs.get("unit", 1)
        self.index = self._kwargs.get("index", 1)
        self.lesson = load_lesson(self.unit, self.index)

        self.make_header("✍ " + self.t("sec_exercise"), back_to="lesson_view")

        sf = ScrollableFrame(self)
        sf.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        for i, task in enumerate(self.lesson.wb_writing, 1):
            self._render_task(sf.inner, i, task)

    def _render_task(self, parent, num, task):
        card = tk.Frame(parent, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=6)
        head = tk.Frame(card, bg=theme.c("card"))
        head.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(head, text=self.t("writing_task_n").format(n=num), font=theme.font("h3"),
                 bg=theme.c("card"), fg=theme.c("accent"),
                 anchor="w").pack(anchor="w")
        prompt = task["prompt"].get(self.i18n.language, "")
        tk.Label(card, text=prompt, font=theme.font("body"),
                 bg=theme.c("card"), fg=theme.c("text"),
                 wraplength=880, justify="left",
                 anchor="w", padx=16, pady=2).pack(fill="x")

        if task["type"] == "order":
            self._render_order(card, task)
        elif task["type"] == "essay":
            self._render_essay(card, task)
        tk.Frame(card, bg=theme.c("card"), height=10).pack()

    def _render_order(self, parent, task):
        words = task["words"][:]
        random.shuffle(words)
        row = tk.Frame(parent, bg=theme.c("bg_soft"))
        row.pack(fill="x", padx=16, pady=6)
        for w in words:
            tk.Label(row, text=w, font=(theme.cjk_family, 14),
                     bg=theme.c("card"), fg=theme.c("text"),
                     padx=8, pady=4).pack(side="left", padx=3, pady=6)

        var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=var, font=(theme.cjk_family, 14),
                         bg=theme.c("bg"), fg=theme.c("text"),
                         relief="flat", highlightthickness=1,
                         highlightbackground=theme.c("border"))
        entry.pack(fill="x", padx=16, pady=(4, 6), ipady=8)

        fb = tk.Label(parent, text="", font=theme.font("body"),
                      bg=theme.c("card"), fg=theme.c("text_muted"),
                      anchor="w", padx=16)
        fb.pack(fill="x")

        def check():
            correct = task["answer"]
            user = var.get().strip().replace(" ", "")
            if user == correct.replace(" ", ""):
                fb.config(text="✓ " + self.t("correct"), fg=theme.c("success"))
            else:
                fb.config(text=f"✗ {self.t('wrong')}.  {self.t('correct_answer')}: {correct}",
                          fg=theme.c("error"))
        tk.Button(parent, text=self.t("check"), font=theme.font("body"),
                  bg=theme.c("accent"), fg="white", relief="flat",
                  padx=16, pady=6, cursor="hand2",
                  command=check).pack(anchor="w", padx=16, pady=(0, 8))

    def _render_essay(self, parent, task):
        req = task["required_words"]
        info = tk.Frame(parent, bg=theme.c("info_bg"))
        info.pack(fill="x", padx=16, pady=(4, 6))
        tk.Label(info, text=self.t("writing_required_words"),
                 font=theme.font("muted"), bg=theme.c("info_bg"),
                 fg=theme.c("info"), anchor="w",
                 padx=12, pady=8).pack(fill="x")
        tk.Label(info, text="  ".join(req), font=(theme.cjk_family, 14),
                 bg=theme.c("info_bg"), fg=theme.c("text"),
                 anchor="w", padx=12, pady=8).pack(fill="x")

        txt = tk.Text(parent, font=(theme.cjk_family, 13), height=8,
                      bg=theme.c("bg"), fg=theme.c("text"),
                      relief="flat", highlightthickness=1,
                      highlightbackground=theme.c("border"), wrap="word")
        txt.pack(fill="x", padx=16, pady=6)

        fb = tk.Label(parent, text="", font=theme.font("body"),
                      bg=theme.c("card"), fg=theme.c("text_muted"),
                      anchor="w", padx=16)
        fb.pack(fill="x")

        def check():
            body = txt.get("1.0", "end").strip()
            length = len([c for c in body if "\u4e00" <= c <= "\u9fff"])
            missing = [w for w in req if w not in body]
            parts = [f"Иероглифов: {length}"]
            if length < task["min_length"]:
                parts.append(f"нужно ≥ {task['min_length']}")
            if missing:
                parts.append("не хватает: " + ", ".join(missing))
            ok = (length >= task["min_length"] and not missing)
            fb.config(text=("✓ " if ok else "• ") + "; ".join(parts),
                      fg=theme.c("success") if ok else theme.c("warn"))
        tk.Button(parent, text=self.t("check"), font=theme.font("body"),
                  bg=theme.c("accent"), fg="white", relief="flat",
                  padx=16, pady=6, cursor="hand2",
                  command=check).pack(anchor="w", padx=16, pady=(0, 8))