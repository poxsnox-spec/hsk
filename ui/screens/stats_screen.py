# -*- coding: utf-8 -*-
"""Экран прогресса: сводка, тепловая карта слов, результаты по урокам."""
import tkinter as tk
from ui.base_screen import BaseScreen
from ui.widgets.scrollable import ScrollableFrame
from core.theme import theme
from core.storage import storage
from models.lesson import load_lesson


class StatsScreen(BaseScreen):

    def _build(self):
        self.make_header(self.t("stats_title"), back_to="main_menu")

        top = tk.Frame(self, bg=theme.c("bg"))
        top.pack(fill="x", padx=24, pady=(0, 8))
        tk.Button(top, text=self.t("stats_refresh"), font=theme.font("body"),
                  bg=theme.c("card"), fg=theme.c("accent_dark"),
                  activebackground=theme.c("accent_soft"),
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._refresh).pack(side="right")

        self.sf = ScrollableFrame(self)
        self.sf.pack(fill="both", expand=True, padx=24, pady=(4, 16))
        self._render()

    def _refresh(self):
        for ch in self.sf.inner.winfo_children():
            ch.destroy()
        self._render()

    # ================================================================
    def _render(self):
        stats = storage.get("vocab_stats", {}) or {}
        scores = storage.get("lesson_scores", {}) or {}
        completed = storage.get("completed_lessons", []) or []

        all_words = []
        for unit, idx in [(1, 1), (1, 2), (1, 3)]:
            try:
                lesson = load_lesson(unit, idx)
                for w in lesson.vocabulary:
                    all_words.append((w.hanzi, w.pinyin, w.translate("ru"),
                                      f"{unit}.{idx}"))
            except Exception:
                pass

        self._render_summary(stats, scores, completed, all_words)
        if all_words:
            self._render_heatmap(stats, all_words)
        if scores:
            self._render_scores(scores)

    # ----------------------------------------------------------------
    def _render_summary(self, stats, scores, completed, all_words):
        total_words = len(all_words)
        touched = sum(1 for hz, *_ in all_words if hz in stats)
        total_attempts = sum(s.get("attempts", 0) for s in scores.values())

        correct_sum = sum(s.get("best", 0) for s in scores.values())
        total_sum = sum(s.get("total", 0) for s in scores.values())
        avg = round(100 * correct_sum / total_sum) if total_sum > 0 else 0

        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text=self.t("stats_summary"), font=theme.font("h3"),
                 bg=theme.c("card"), fg=theme.c("accent"),
                 anchor="w", padx=20, pady=14).pack(fill="x")

        rows = [
            (self.t("stats_words_learned"),  f"{touched} / {total_words}"),
            (self.t("stats_avg_score"),      f"{avg}%"),
            (self.t("stats_total_attempts"), str(total_attempts)),
            (self.t("stats_lessons_done"),   str(len(completed))),
        ]
        for label, value in rows:
            row = tk.Frame(card, bg=theme.c("card"))
            row.pack(fill="x", padx=20, pady=2)
            tk.Label(row, text=label, font=theme.font("body"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     anchor="w", width=24).pack(side="left")
            tk.Label(row, text=value, font=theme.font("body_bold"),
                     bg=theme.c("card"), fg=theme.c("text"),
                     anchor="w").pack(side="left")

        tk.Frame(card, bg=theme.c("card"), height=12).pack()

    # ----------------------------------------------------------------
    def _render_heatmap(self, stats, all_words):
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text=self.t("stats_heatmap"),
                 font=theme.font("h3"),
                 bg=theme.c("card"), fg=theme.c("accent"),
                 anchor="w", padx=20, pady=14).pack(fill="x")

        legend = tk.Frame(card, bg=theme.c("card"))
        legend.pack(fill="x", padx=20, pady=(0, 8))
        for label, color in [
            (self.t("stats_legend_new"), theme.c("bg_soft")),
            ("< 50%",                    theme.c("error_bg")),
            ("50–79%",                   "#FFF1C7"),
            ("≥ 80%",                    theme.c("success_bg")),
        ]:
            tk.Label(legend, text="  ", bg=color, width=3,
                     highlightbackground=theme.c("border"),
                     highlightthickness=1).pack(side="left", padx=4)
            tk.Label(legend, text=label, font=theme.font("muted"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     padx=12).pack(side="left")

        grid = tk.Frame(card, bg=theme.c("card"))
        grid.pack(fill="x", padx=20, pady=(4, 16))

        cols = 6
        for i, (hanzi, pinyin, tr, label) in enumerate(all_words):
            rec = stats.get(hanzi)
            if rec is None or rec.get("seen", 0) == 0:
                bg = theme.c("bg_soft")
                fg = theme.c("text_muted")
                pct = "—"
            else:
                pct = round(100 * rec["correct"] / rec["seen"])
                if pct < 50:
                    bg = theme.c("error_bg")
                    fg = theme.c("error")
                elif pct < 80:
                    bg = "#FFF1C7"
                    fg = "#8B6914"
                else:
                    bg = theme.c("success_bg")
                    fg = theme.c("success")

            cell = tk.Frame(grid, bg=bg,
                            highlightbackground=theme.c("border"),
                            highlightthickness=1)
            cell.grid(row=i // cols, column=i % cols,
                      padx=3, pady=3, sticky="nsew")

            tk.Label(cell, text=hanzi, font=(theme.cjk_family, 18, "bold"),
                     bg=bg, fg=fg, pady=6, padx=6).pack()
            tk.Label(cell, text=f"{pct}%" if pct != "—" else "—",
                     font=theme.font("muted"), bg=bg, fg=fg,
                     pady=4).pack()

        for c in range(cols):
            grid.grid_columnconfigure(c, weight=1, uniform="heat")

    # ----------------------------------------------------------------
    def _render_scores(self, scores):
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text=self.t("stats_scores"),
                 font=theme.font("h3"),
                 bg=theme.c("card"), fg=theme.c("accent"),
                 anchor="w", padx=20, pady=14).pack(fill="x")

        header = tk.Frame(card, bg=theme.c("bg_soft"))
        header.pack(fill="x", padx=20)
        for txt, w in [(self.t("stats_col_lesson"), 32),
                       (self.t("stats_col_best"), 10),
                       (self.t("stats_col_total"), 10),
                       (self.t("stats_col_attempts"), 10)]:
            tk.Label(header, text=txt, font=theme.font("muted"),
                     bg=theme.c("bg_soft"), fg=theme.c("text_muted"),
                     anchor="w", width=w, padx=8, pady=6).pack(side="left")

        for key, rec in sorted(scores.items()):
            row = tk.Frame(card, bg=theme.c("card"))
            row.pack(fill="x", padx=20)
            tk.Label(row, text=key, font=theme.font("body"),
                     bg=theme.c("card"), fg=theme.c("text"),
                     anchor="w", width=32, padx=8, pady=4).pack(side="left")
            tk.Label(row, text=str(rec.get("best", 0)), font=theme.font("body_bold"),
                     bg=theme.c("card"), fg=theme.c("success"),
                     anchor="w", width=10, padx=8).pack(side="left")
            tk.Label(row, text=str(rec.get("total", 0)), font=theme.font("body"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     anchor="w", width=10, padx=8).pack(side="left")
            tk.Label(row, text=str(rec.get("attempts", 0)), font=theme.font("body"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     anchor="w", width=10, padx=8).pack(side="left")
            tk.Frame(card, bg=theme.c("border"), height=1).pack(fill="x", padx=20)

        tk.Frame(card, bg=theme.c("card"), height=12).pack()