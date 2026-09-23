# -*- coding: utf-8 -*-
"""Урок: 8 разделов во вкладках."""
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from models.lesson import load_lesson
from core.audio import audio


class LessonViewScreen(BaseScreen):
    def _build(self):
        self.unit = self._kwargs.get("unit", 1)
        self.index = self._kwargs.get("index", 1)
        self.lesson = load_lesson(self.unit, self.index)

        self.make_header(self.lesson.title_in(self.i18n.language), back_to="lessons")

        head = tk.Frame(self, bg=theme.c("bg"))
        head.pack(fill="x", padx=28, pady=(4, 10))
        tk.Label(head, text=self.lesson.title.get("zh", ""),
                 font=(theme.cjk_family, 28, "bold"),
                 bg=theme.c("bg"), fg=theme.c("accent")).pack(anchor="w")
        tk.Label(head, text=self.lesson.title_in(self.i18n.language),
                 font=theme.font("h3"), bg=theme.c("bg"),
                 fg=theme.c("text_muted")).pack(anchor="w")

        tabs_bar = tk.Frame(self, bg=theme.c("bg"))
        tabs_bar.pack(fill="x", padx=20)

        self.tabs = [
            ("sec_text", "text"), ("sec_vocab", "vocab"),
            ("sec_grammar", "grammar"), ("sec_phrases", "phrases"),
            ("sec_compare", "compare"), ("sec_exercise", "exercise"),
            ("sec_extend", "extend"), ("sec_apply", "apply"),
        ]
        self.tab_btns = {}
        for key, name in self.tabs:
            btn = tk.Button(tabs_bar, text=self.t(key), font=theme.font("body"),
                            bg=theme.c("bg"), fg=theme.c("text_muted"),
                            activebackground=theme.c("accent_soft"),
                            relief="flat", padx=10, pady=8, cursor="hand2",
                            command=lambda n=name: self._switch(n))
            btn.pack(side="left", padx=2)
            self.tab_btns[name] = btn

        self.content = tk.Frame(self, bg=theme.c("bg"))
        self.content.pack(fill="both", expand=True, padx=20, pady=(10, 16))
        self.current = None
        self._switch("text")

    def _switch(self, name):
        for child in self.content.winfo_children():
            child.destroy()
        self.current = name
        for n, btn in self.tab_btns.items():
            active = (n == name)
            btn.configure(bg=theme.c("accent") if active else theme.c("bg"),
                          fg="white" if active else theme.c("text_muted"))
        {
            "text": self._render_text, "vocab": self._render_vocab,
            "grammar": self._render_grammar, "phrases": self._render_phrases,
            "compare": self._render_compare, "exercise": self._render_exercise,
            "extend": self._render_extend, "apply": self._render_apply,
        }[name]()

    def _render_text(self):
        from ui.widgets.scrollable import ScrollableFrame
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)

        ctrl = tk.Frame(sf.inner, bg=theme.c("bg"))
        ctrl.pack(fill="x", pady=(0, 8))
        self._audio_btn(ctrl, "🔊 " + self.t("sec_text"), "textbook_1")
        self._audio_btn(ctrl, "🔊 " + self.t("sec_text") + " (2)", "textbook_2")

        box = tk.Frame(sf.inner, bg=theme.c("card"),
                       highlightbackground=theme.c("border"),
                       highlightthickness=1)
        box.pack(fill="x", pady=6)
        tk.Label(box, text=self.lesson.text_zh,
                 font=(theme.cjk_family, 14), bg=theme.c("card"),
                 fg=theme.c("text"), wraplength=900, justify="left",
                 anchor="w", padx=20, pady=18).pack(fill="x")

        tr = self.lesson.text_translation.get(self.i18n.language, "")
        if tr:
            tk.Label(sf.inner, text=tr, font=theme.font("body"),
                     bg=theme.c("bg"), fg=theme.c("text_muted"),
                     wraplength=900, justify="left").pack(fill="x", pady=(6, 12))

    def _audio_btn(self, parent, text, key):
        fname = self.lesson.audio_files.get(key, "")
        has = fname and audio.exists(self.unit, self.index, fname)
        tk.Button(parent, text=text, font=theme.font("body"),
                  bg=theme.c("card") if has else theme.c("bg_soft"),
                  fg=theme.c("accent") if has else theme.c("text_muted"),
                  activebackground=theme.c("accent_soft"),
                  relief="flat", padx=12, pady=6,
                  cursor="hand2" if has else "",
                  state="normal" if has else "disabled",
                  command=(lambda f=fname: audio.play(
                      audio.find(self.unit, self.index, f))) if has else None,
                  ).pack(side="left", padx=(0, 8))

    def _render_vocab(self):
        from ui.widgets.scrollable import ScrollableFrame
        from ui.widgets.hanzi_card import HanziCard
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)

        row = tk.Frame(sf.inner, bg=theme.c("bg"))
        row.pack(fill="x", pady=(0, 8))
        tk.Label(row, text=f"生词 · {len(self.lesson.vocabulary)}",
                 font=theme.font("h3"), bg=theme.c("bg"),
                 fg=theme.c("text")).pack(side="left")
        tk.Button(row, text="🃏 " + self.t("flashcards"),
                  font=theme.font("body"), bg=theme.c("accent"),
                  fg="white", relief="flat", padx=12, pady=6, cursor="hand2",
                  command=self._open_flashcards).pack(side="right")

        grid = tk.Frame(sf.inner, bg=theme.c("bg"))
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=1, uniform="v")
        grid.grid_columnconfigure(1, weight=1, uniform="v")

        for i, w in enumerate(self.lesson.vocabulary):
            card = HanziCard(grid, w, unit=self.unit, lesson=self.index)
            card.grid(row=i // 2, column=i % 2, sticky="ew", padx=6, pady=4)

    def _render_grammar(self):
        from ui.widgets.scrollable import ScrollableFrame
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)

        for gp in self.lesson.grammar:
            box = tk.Frame(sf.inner, bg=theme.c("card"),
                           highlightbackground=theme.c("border"),
                           highlightthickness=1)
            box.pack(fill="x", pady=6)

            top = tk.Frame(box, bg=theme.c("card"))
            top.pack(fill="x", padx=16, pady=(12, 4))
            tk.Label(top, text=gp.word, font=(theme.cjk_family, 24, "bold"),
                     bg=theme.c("card"), fg=theme.c("accent")).pack(side="left")
            tk.Label(top, text=f"  {gp.pos}", font=theme.font("muted"),
                     bg=theme.c("card"), fg=theme.c("text_muted")).pack(side="left")

            tk.Label(box, text=gp.explanation.get(self.i18n.language, ""),
                     font=theme.font("body"), bg=theme.c("card"),
                     fg=theme.c("text"), wraplength=900, justify="left",
                     anchor="w", padx=16).pack(fill="x", pady=(4, 8))

            for i, ex in enumerate(gp.examples, 1):
                ex_box = tk.Frame(box, bg=theme.c("bg_soft"))
                ex_box.pack(fill="x", padx=16, pady=3)
                tk.Label(ex_box, text=f"{i}. {ex['zh']}",
                         font=(theme.cjk_family, 13), bg=theme.c("bg_soft"),
                         fg=theme.c("text"), wraplength=880,
                         justify="left", anchor="w", padx=10, pady=6).pack(fill="x")
                tr = ex.get(self.i18n.language, "")
                if tr:
                    tk.Label(ex_box, text=tr, font=theme.font("muted"),
                             bg=theme.c("bg_soft"), fg=theme.c("text_muted"),
                             wraplength=880, justify="left",
                             anchor="w", padx=10, pady=6).pack(fill="x")

            tk.Frame(box, bg=theme.c("card"), height=8).pack()

    def _render_phrases(self):
        from ui.widgets.scrollable import ScrollableFrame
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)
        for col in self.lesson.collocations:
            box = tk.Frame(sf.inner, bg=theme.c("card"),
                           highlightbackground=theme.c("border"),
                           highlightthickness=1)
            box.pack(fill="x", pady=6)
            tk.Label(box, text=col["pattern"], font=theme.font("h3"),
                     bg=theme.c("card"), fg=theme.c("accent"),
                     anchor="w", padx=16, pady=12).pack(fill="x")
            for item in col["items"]:
                tk.Label(box, text="· " + item, font=(theme.cjk_family, 13),
                         bg=theme.c("card"), fg=theme.c("text"),
                         anchor="w", padx=28, pady=2).pack(fill="x")
            tk.Frame(box, bg=theme.c("card"), height=8).pack()

    def _render_compare(self):
        from ui.widgets.scrollable import ScrollableFrame
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)
        for cp in self.lesson.comparisons:
            box = tk.Frame(sf.inner, bg=theme.c("card"),
                           highlightbackground=theme.c("border"),
                           highlightthickness=1)
            box.pack(fill="x", pady=8)
            head = tk.Frame(box, bg=theme.c("accent_soft"))
            head.pack(fill="x")
            tk.Label(head, text=f"{cp.word_a}   vs   {cp.word_b}",
                     font=(theme.cjk_family, 20, "bold"),
                     bg=theme.c("accent_soft"), fg=theme.c("accent_dark"),
                     pady=10).pack()
            tk.Label(box, text="≈ " + cp.common.get(self.i18n.language, ""),
                     font=theme.font("body"), bg=theme.c("card"),
                     fg=theme.c("text"), wraplength=900, justify="left",
                     anchor="w", padx=16, pady=10).pack(fill="x")
            tk.Label(box, text="≠ " + self.t("sec_compare"),
                     font=theme.font("h3"), bg=theme.c("card"),
                     fg=theme.c("text"), anchor="w", padx=16).pack(fill="x")
            for d in cp.differences:
                tk.Label(box, text="— " + d.get(self.i18n.language, ""),
                         font=theme.font("body"), bg=theme.c("card"),
                         fg=theme.c("text_muted"), wraplength=900,
                         justify="left", anchor="w", padx=28, pady=2).pack(fill="x")
            tk.Frame(box, bg=theme.c("card"), height=10).pack()

    def _render_exercise(self):
        wrap = tk.Frame(self.content, bg=theme.c("bg"))
        wrap.pack(fill="both", expand=True)
        tk.Label(wrap, text="📝 " + self.t("sec_exercise"),
                 font=theme.font("h2"), bg=theme.c("bg"),
                 fg=theme.c("text")).pack(anchor="w", pady=(0, 12))
        cards = [
            ("🎧 听力", "Listening · аудио workbook_01-1/2.mp3", self._open_listening),
            ("📖 阅读", "Reading · выбор правильного варианта", self._open_reading),
            ("✍ 书写", "Writing · 3 предложения + эссе", self._open_writing),
        ]
        for title, subtitle, cmd in cards:
            card = tk.Frame(wrap, bg=theme.c("card"),
                            highlightbackground=theme.c("border"),
                            highlightthickness=1, cursor="hand2")
            card.pack(fill="x", pady=6)
            box = tk.Frame(card, bg=theme.c("card"))
            box.pack(fill="x", padx=20, pady=16)
            tk.Label(box, text=title, font=theme.font("h3"),
                     bg=theme.c("card"), fg=theme.c("accent"),
                     anchor="w").pack(anchor="w")
            tk.Label(box, text=subtitle, font=theme.font("muted"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     anchor="w").pack(anchor="w")
            for w in (card, box, *box.winfo_children()):
                w.bind("<Button-1>", lambda _e, c=cmd: c())

    def _render_extend(self):
        from ui.widgets.scrollable import ScrollableFrame
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)
        if self.lesson.expansion:
            tk.Label(sf.inner,
                     text=self.lesson.expansion.get("topic", {}).get(self.i18n.language, ""),
                     font=theme.font("h3"), bg=theme.c("bg"),
                     fg=theme.c("text")).pack(anchor="w", pady=(0, 8))
            for w in self.lesson.expansion.get("words", []):
                card = tk.Frame(sf.inner, bg=theme.c("card"),
                                highlightbackground=theme.c("border"),
                                highlightthickness=1)
                card.pack(fill="x", pady=3)
                row = tk.Frame(card, bg=theme.c("card"))
                row.pack(fill="x", padx=16, pady=10)
                tk.Label(row, text=w["hanzi"], font=(theme.cjk_family, 20, "bold"),
                         bg=theme.c("card"), fg=theme.c("accent")).pack(side="left")
                tk.Label(row, text=f"  {w['pinyin']}", font=theme.font("pinyin_s"),
                         bg=theme.c("card"), fg=theme.c("text_muted")).pack(side="left")
                tk.Label(row, text=w["meaning"].get(self.i18n.language, ""),
                         font=theme.font("body"), bg=theme.c("card"),
                         fg=theme.c("text")).pack(side="right")

    def _render_apply(self):
        from ui.widgets.scrollable import ScrollableFrame
        sf = ScrollableFrame(self.content)
        sf.pack(fill="both", expand=True)
        box = tk.Frame(sf.inner, bg=theme.c("info_bg"),
                       highlightbackground=theme.c("info"),
                       highlightthickness=1)
        box.pack(fill="x", pady=8)
        tk.Label(box, text="🎓 " + self.t("sec_apply"),
                 font=theme.font("h3"), bg=theme.c("info_bg"),
                 fg=theme.c("info"), anchor="w", padx=20, pady=14).pack(fill="x")
        txt = self.lesson.application.get("discussion", {}).get(self.i18n.language, "")
        tk.Label(box, text=txt, font=theme.font("body"), bg=theme.c("info_bg"),
                 fg=theme.c("text"), wraplength=900, justify="left",
                 anchor="w", padx=20, pady=16).pack(fill="x")

        # --- Отметка урока как пройденного ---
        from core.storage import storage
        lesson_id = f"unit{self.unit}_lesson{self.index}"
        is_done = lesson_id in storage.get("completed_lessons", [])

        if is_done:
            tk.Label(sf.inner, text=self.t("lesson_is_done"),
                     font=theme.font("h3"), bg=theme.c("bg"),
                     fg=theme.c("success"), pady=16).pack()
        else:
            def _mark():
                storage.mark_lesson_complete(lesson_id)
                self._switch("apply")
            tk.Button(sf.inner, text=self.t("lesson_mark_done"),
                      font=theme.font("h3"),
                      bg=theme.c("success"), fg="white",
                      activebackground="#1B5E20",
                      relief="flat", padx=20, pady=12, cursor="hand2",
                      command=_mark).pack(pady=16)

    def _open_flashcards(self):
        self.manager.show("flashcards", unit=self.unit, index=self.index)

    def _open_listening(self):
        self.manager.show("exercise", unit=self.unit, index=self.index, mode="listening")

    def _open_reading(self):
        self.manager.show("exercise", unit=self.unit, index=self.index, mode="reading")

    def _open_writing(self):
        self.manager.show("writing", unit=self.unit, index=self.index)