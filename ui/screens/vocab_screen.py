# -*- coding: utf-8 -*-
"""Словарь: ttk.Treeview с колонкой «Урок», сортировкой и цветом юнита."""
import csv
import tkinter as tk
from tkinter import ttk

from ui.base_screen import BaseScreen
from core.theme import theme
from core.audio import audio
from core.config import USER_DATA_DIR
from models.lesson import load_lesson


# Цвета по юнитам (мягкие, чтобы не утомляли)
UNIT_COLORS_LIGHT = {
    1: "#FFF3E0",  # оранжевый
    2: "#E8F5E9",  # зелёный
    3: "#E3F2FD",  # синий
    4: "#F3E5F5",  # фиолетовый
    5: "#FFF9C4",  # жёлтый
    6: "#FCE4EC",  # розовый
}
UNIT_COLORS_DARK = {
    1: "#3D2A1A",
    2: "#1E3622",
    3: "#1A2A3A",
    4: "#2A1F2E",
    5: "#3A3520",
    6: "#3A1F26",
}


class VocabScreen(BaseScreen):

    def _build(self):
        self.make_header(self.t("vocab_title"), back_to="main_menu")

        # --- Собираем все слова ---
        self.all_words = []
        for unit in range(1, 7):
            for idx in range(1, 4):
                try:
                    lesson = load_lesson(unit, idx)
                except Exception:
                    continue
                label = f"{unit}.{idx}"
                for w in lesson.vocabulary:
                    self.all_words.append({
                        "unit": unit, "index": idx, "label": label, "w": w,
                    })

        self.tree = None
        self._sort_col = None
        self._sort_reverse = False

        # --- Панель управления ---
        ctrl = tk.Frame(self, bg=theme.c("bg"))
        ctrl.pack(fill="x", padx=24, pady=(4, 8))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            ctrl, textvariable=self.search_var,
            font=theme.font("body"),
            bg=theme.c("card"), fg=theme.c("text"),
            insertbackground=theme.c("text"),
            relief="flat", highlightthickness=1,
            highlightbackground=theme.c("border"),
            highlightcolor=theme.c("accent"),
        )
        self.search_entry.pack(side="left", fill="x", expand=True,
                               ipady=int(8 * theme.scale), padx=(0, 8))
        self._set_placeholder(self.search_entry, self.t("vocab_search"))

        # Фильтр по урокам
        self.filter_var = tk.StringVar(value=self.t("vocab_filter_all"))
        labels = [self.t("vocab_filter_all")] + sorted(
            {item["label"] for item in self.all_words}, key=self._sort_label
        )
        self._filter_map = {self.t("vocab_filter_all"): None}
        for lbl in labels[1:]:
            self._filter_map[lbl] = lbl

        om = tk.OptionMenu(ctrl, self.filter_var, *labels,
                           command=lambda _v: self._refresh())
        om.config(font=theme.font("body"), bg=theme.c("card"),
                  fg=theme.c("text"),
                  activebackground=theme.c("accent_soft"),
                  relief="flat", padx=10, highlightthickness=0)
        om["menu"].config(font=theme.font("body"),
                          bg=theme.c("card"), fg=theme.c("text"))
        om.pack(side="left", padx=(0, 8))

        tk.Button(ctrl, text=self.t("vocab_export"), font=theme.font("body"),
                  bg=theme.c("card"), fg=theme.c("accent_dark"),
                  activebackground=theme.c("accent_soft"),
                  relief="flat", padx=int(12 * theme.scale),
                  pady=int(6 * theme.scale), cursor="hand2",
                  command=self._export_csv).pack(side="left")

        # --- Строка статуса ---
        self.status = tk.Label(self, text="", font=theme.font("muted"),
                               bg=theme.c("bg"), fg=theme.c("text_muted"))
        self.status.pack(fill="x", padx=24, pady=(0, 2))

        # Подсказка
        tk.Label(self, text=self.t("vocab_hint_sort"),
                 font=theme.font("muted"), bg=theme.c("bg"),
                 fg=theme.c("text_muted")).pack(fill="x", padx=24, pady=(0, 4))

        # --- Treeview ---
        self._setup_treeview_style()

        wrap = tk.Frame(self, bg=theme.c("bg"))
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        # ВАЖНО: колонка "lesson" идёт первой
        cols = ("lesson", "hanzi", "pinyin", "pos", "ru", "tk", "en")
        self.tree = ttk.Treeview(
            wrap, columns=cols, show="headings",
            style="Vocab.Treeview", selectmode="browse",
        )

        self.tree.heading("lesson", text=self.t("vocab_col_lesson"),
                          command=lambda: self._sort_by("lesson"))
        self.tree.heading("hanzi",  text=self.t("vocab_col_hanzi"),
                          command=lambda: self._sort_by("hanzi"))
        self.tree.heading("pinyin", text=self.t("vocab_col_pinyin"),
                          command=lambda: self._sort_by("pinyin"))
        self.tree.heading("pos",    text=self.t("vocab_col_pos"),
                          command=lambda: self._sort_by("pos"))
        self.tree.heading("ru",     text=self.t("vocab_col_ru"),
                          command=lambda: self._sort_by("ru"))
        self.tree.heading("tk",     text=self.t("vocab_col_tk"),
                          command=lambda: self._sort_by("tk"))
        self.tree.heading("en",     text=self.t("vocab_col_en"),
                          command=lambda: self._sort_by("en"))

        s = theme.scale
        self.tree.column("lesson", width=int(70 * s),  anchor="center")
        self.tree.column("hanzi",  width=int(90 * s),  anchor="w")
        self.tree.column("pinyin", width=int(120 * s), anchor="w")
        self.tree.column("pos",    width=int(70 * s),  anchor="w")
        self.tree.column("ru",     width=int(220 * s), anchor="w")
        self.tree.column("tk",     width=int(210 * s), anchor="w")
        self.tree.column("en",     width=int(210 * s), anchor="w")

        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Цветовые теги для юнитов
        colors = (UNIT_COLORS_DARK if theme.mode == "dark"
                  else UNIT_COLORS_LIGHT)
        for unit, color in colors.items():
            self.tree.tag_configure(f"unit{unit}", background=color)
        self.tree.tag_configure("stripe", background=theme.c("card"))

        # Двойной клик — аудио
        self.tree.bind("<Double-1>", self._on_double_click)

        # Поиск
        self.search_var.trace_add("write", lambda *_: self._refresh())

        self._refresh()

    # ================================================================
    def _sort_label(self, lbl):
        try:
            u, l = lbl.split(".")
            return (int(u), int(l))
        except Exception:
            return (99, 99)

    def _set_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(fg=theme.c("text_muted"))

        def on_focus_in(_e):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg=theme.c("text"))

        def on_focus_out(_e):
            if not entry.get().strip():
                entry.delete(0, "end")
                entry.insert(0, text)
                entry.config(fg=theme.c("text_muted"))

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _setup_treeview_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        row_h = int(30 * theme.scale)

        style.configure(
            "Vocab.Treeview",
            background=theme.c("card"),
            foreground=theme.c("text"),
            fieldbackground=theme.c("card"),
            rowheight=row_h,
            font=theme.font("body"),
            borderwidth=0,
        )
        style.configure(
            "Vocab.Treeview.Heading",
            background=theme.c("bg_soft"),
            foreground=theme.c("text"),
            font=theme.font("body_bold"),
            relief="flat",
        )
        style.map(
            "Vocab.Treeview",
            background=[("selected", theme.c("accent_soft"))],
            foreground=[("selected", theme.c("text"))],
        )
        style.map(
            "Vocab.Treeview.Heading",
            background=[("active", theme.c("accent_soft"))],
        )

    # ================================================================
    def _get_query(self):
        q = self.search_var.get().strip().lower()
        placeholder = self.t("vocab_search").lower()
        if q == placeholder or not q:
            return ""
        return q

    def _matches(self, item, query):
        w = item["w"]
        haystack = " ".join([
            item["label"], w.hanzi, w.pinyin, w.pos,
            w.translate("ru"), w.translate("tk"), w.translate("en"),
        ]).lower()
        return query in haystack

    def _refresh(self):
        if self.tree is None:
            return

        for iid in self.tree.get_children():
            self.tree.delete(iid)

        query = self._get_query()
        lesson_filter = self._filter_map.get(self.filter_var.get())

        items = []
        for item in self.all_words:
            if lesson_filter and item["label"] != lesson_filter:
                continue
            if query and not self._matches(item, query):
                continue
            items.append(item)

        # Сортировка
        if self._sort_col:
            items = self._sort_items(items, self._sort_col, self._sort_reverse)

        for item in items:
            w = item["w"]
            self.tree.insert(
                "", "end",
                iid=str(id(item)),
                values=(
                    item["label"],          # ← колонка «Урок»
                    w.hanzi,
                    w.pinyin,
                    w.pos,
                    w.translate("ru"),
                    w.translate("tk"),
                    w.translate("en"),
                ),
                tags=(f"unit{item['unit']}",),
            )

        self.status.config(
            text=f"{self.t('vocab_count')}: {len(items)}   ·   "
                 f"{self.t('vocab_total')}: {len(self.all_words)}"
        )

    def _sort_items(self, items, col, reverse):
        def key(item):
            w = item["w"]
            if col == "lesson":
                return self._sort_label(item["label"])
            if col == "hanzi":
                return w.hanzi
            if col == "pinyin":
                return w.pinyin
            if col == "pos":
                return w.pos
            if col == "ru":
                return w.translate("ru").lower()
            if col == "tk":
                return w.translate("tk").lower()
            if col == "en":
                return w.translate("en").lower()
            return ""

        return sorted(items, key=key, reverse=reverse)

    def _sort_by(self, col):
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False
        self._refresh()

    # ================================================================
    def _on_double_click(self, event):
        if self.tree is None:
            return
        iid = self.tree.identify_row(event.y)
        if not iid:
            return
        try:
            item_id = int(iid)
        except ValueError:
            return
        for item in self.all_words:
            if id(item) == item_id:
                w = item["w"]
                af = getattr(w, "audio", "") or ""
                if af and audio.exists(item["unit"], item["index"], af):
                    audio.play(audio.find(item["unit"], item["index"], af))
                return

    # ================================================================
    def _export_csv(self):
        out = USER_DATA_DIR / "vocabulary.csv"
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Lesson", "Hanzi", "Pinyin", "POS",
                             "RU", "TK", "EN"])
            for item in self.all_words:
                w = item["w"]
                writer.writerow([
                    item["label"],
                    w.hanzi, w.pinyin, w.pos,
                    w.translate("ru"), w.translate("tk"), w.translate("en"),
                ])
        from tkinter import messagebox
        messagebox.showinfo(
            self.t("vocab_export"),
            f"{self.t('vocab_export_done')}:\n{out}",
        )
