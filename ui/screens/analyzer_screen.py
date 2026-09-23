# -*- coding: utf-8 -*-
"""Анализатор иероглифов: радикал, черты, компоненты, разбор пиньиня."""
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from models.lesson import load_lesson
from data.hanzi_db import analyze, split_pinyin, TONE_NAMES


class AnalyzerScreen(BaseScreen):
    def _build(self):
        self.unit = self._kwargs.get("unit", 1)
        self.index = self._kwargs.get("index", 1)
        self.lesson = load_lesson(self.unit, self.index)

        self.make_header(self.t("analyzer_title"), back_to="lesson_view")

        top = tk.Frame(self, bg=theme.c("bg"))
        top.pack(fill="x", padx=24, pady=(0, 10))
        tk.Label(top, text=self.t("analyzer_word"), font=theme.font("body"),
                 bg=theme.c("bg"), fg=theme.c("text_muted")).pack(side="left")

        self.selected = self.lesson.vocabulary[0]
        self.var = tk.StringVar(value=self.selected.hanzi)
        options = [w.hanzi for w in self.lesson.vocabulary]
        om = tk.OptionMenu(top, self.var, *options, command=self._on_pick)
        om.config(font=(theme.cjk_family, 14), bg=theme.c("card"),
                  fg=theme.c("text"), relief="flat", padx=12,
                  highlightthickness=0)
        om["menu"].config(font=(theme.cjk_family, 12))
        om.pack(side="left", padx=8)

        self.result_frame = tk.Frame(self, bg=theme.c("bg"))
        self.result_frame.pack(fill="both", expand=True, padx=24, pady=8)
        self._render(self.selected)

    def _on_pick(self, hanzi):
        for w in self.lesson.vocabulary:
            if w.hanzi == hanzi:
                self.selected = w
                break
        self._render(self.selected)

    def _render(self, word):
        for ch in self.result_frame.winfo_children():
            ch.destroy()

        card = tk.Frame(self.result_frame, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=6)
        top_row = tk.Frame(card, bg=theme.c("card"))
        top_row.pack(fill="x", padx=20, pady=16)
        tk.Label(top_row, text=word.hanzi, font=(theme.cjk_family, 56, "bold"),
                 bg=theme.c("card"), fg=theme.c("accent")).pack(side="left")
        info = tk.Frame(top_row, bg=theme.c("card"))
        info.pack(side="left", padx=20)
        tk.Label(info, text=word.pinyin, font=theme.font("pinyin"),
                 bg=theme.c("card"), fg=theme.c("text_muted")).pack(anchor="w")
        tk.Label(info, text=f"({word.pos})  {word.translate(self.i18n.language)}",
                 font=theme.font("body"), bg=theme.c("card"),
                 fg=theme.c("text")).pack(anchor="w")

        self._render_pinyin(word)
        for i, ch in enumerate(word.hanzi):
            self._render_char(ch)

    def _render_pinyin(self, word):
        s = tk.Frame(self.result_frame, bg=theme.c("bg_soft"))
        s.pack(fill="x", pady=4)
        tk.Label(s, text=self.t("analyzer_pinyin_split"), font=theme.font("h3"),
                 bg=theme.c("bg_soft"), fg=theme.c("text"),
                 anchor="w", padx=16, pady=(10, 4)).pack(fill="x")
        row = tk.Frame(s, bg=theme.c("bg_soft"))
        row.pack(fill="x", padx=16, pady=(0, 12))
        for syl in split_pinyin(word.pinyin):
            box = tk.Frame(row, bg=theme.c("card"),
                           highlightbackground=theme.c("border"),
                           highlightthickness=1)
            box.pack(side="left", padx=4)
            tk.Label(box, text=syl["display"], font=(theme.ui_family, 18, "bold"),
                     bg=theme.c("card"), fg=theme.c("accent")).pack(padx=14, pady=(8, 0))
            tk.Label(box, text=f"тон {syl['tone']}", font=theme.font("muted"),
                     bg=theme.c("card"), fg=theme.c("text_muted")).pack()
            tk.Label(box, text=TONE_NAMES[syl["tone"]].get(self.i18n.language, ""),
                     font=theme.font("muted"), bg=theme.c("card"),
                     fg=theme.c("text_muted"), wraplength=140,
                     justify="center").pack(padx=10, pady=(0, 8))

    def _render_char(self, ch):
        meta = analyze(ch)
        card = tk.Frame(self.result_frame, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=4)
        head = tk.Frame(card, bg=theme.c("card"))
        head.pack(fill="x", padx=20, pady=12)
        tk.Label(head, text=ch, font=(theme.cjk_family, 42, "bold"),
                 bg=theme.c("card"), fg=theme.c("text")).pack(side="left", padx=(0, 20))
        if meta is None:
            tk.Label(head, text=self.t("analyzer_no_data"),
                     font=theme.font("body"), bg=theme.c("card"),
                     fg=theme.c("text_muted")).pack(side="left")
            return
        info = tk.Frame(head, bg=theme.c("card"))
        info.pack(side="left", fill="x", expand=True)
        self._kv(info, self.t("analyzer_radical"), f"{meta['radical']}  ({meta.get('radical_ru','')})")
        self._kv(info, "Черт:", str(meta["strokes"]))
        self._kv(info, self.t("analyzer_components"), " + ".join(meta["components"]))

    def _kv(self, parent, k, v):
        row = tk.Frame(parent, bg=theme.c("card"))
        row.pack(anchor="w", pady=1)
        tk.Label(row, text=k, font=theme.font("muted"),
                 bg=theme.c("card"), fg=theme.c("text_muted"),
                 width=18, anchor="w").pack(side="left")
        tk.Label(row, text=v, font=(theme.cjk_family, 13),
                 bg=theme.c("card"), fg=theme.c("text"),
                 anchor="w").pack(side="left")