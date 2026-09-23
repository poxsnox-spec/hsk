# -*- coding: utf-8 -*-
"""SRS-сессия на алгоритме SM-2 (Again / Hard / Good / Easy)."""
import random
from datetime import datetime
import tkinter as tk
from ui.base_screen import BaseScreen
from ui.widgets.scrollable import ScrollableFrame
from core.theme import theme
from core.storage import (storage, RATING_AGAIN, RATING_HARD,
                          RATING_GOOD, RATING_EASY)
from core.audio import audio
from models.lesson import load_lesson


SESSION_SIZE = 20


def _fmt_interval(due_iso: str) -> str:
    """Сколько осталось до следующего повторения."""
    try:
        due = datetime.fromisoformat(due_iso)
    except Exception:
        return ""
    now = datetime.now()
    delta = due - now
    secs = int(delta.total_seconds())
    if secs <= 30:
        return "now"
    if secs < 3600:
        return f"min:{max(1, secs // 60)}"
    if secs < 86400 * 2:
        hours = max(1, secs // 3600)
        return f"min:{hours * 60}"
    days = max(1, secs // 86400)
    return f"days:{days}"


class SrsScreen(BaseScreen):

    def _build(self):
        self.make_header(self.t("srs_title"), back_to="main_menu")

        # Загружаем слова
        self.all_words = []
        for unit in range(1, 7):
            for idx in range(1, 4):
                try:
                    lesson = load_lesson(unit, idx)
                except Exception:
                    continue
                for w in lesson.vocabulary:
                    self.all_words.append((unit, idx, w))

        # Панель
        top = tk.Frame(self, bg=theme.c("bg"))
        top.pack(fill="x", padx=24, pady=(0, 8))
        tk.Button(top, text=self.t("srs_start"), font=theme.font("body"),
                  bg=theme.c("accent"), fg="white",
                  activebackground=theme.c("accent_dark"),
                  relief="flat", padx=16, pady=8, cursor="hand2",
                  command=self._start_session).pack(side="left")

        self.sf = ScrollableFrame(self)
        self.sf.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        # Горячие клавиши для сессии
        self.bind_all("<space>", lambda _e: self._hotkey_space())
        self.bind_all("<Key-1>", lambda _e: self._hotkey(1))
        self.bind_all("<Key-2>", lambda _e: self._hotkey(2))
        self.bind_all("<Key-3>", lambda _e: self._hotkey(3))
        self.bind_all("<Key-4>", lambda _e: self._hotkey(4))

        self.session_active = False
        self._render_home()

    # ================================================================
    def _hotkey_space(self):
        if self.session_active and not self.flipped:
            self._reveal()

    def _hotkey(self, n):
        if not self.session_active or not self.flipped:
            return
        mapping = {1: RATING_AGAIN, 2: RATING_HARD, 3: RATING_GOOD, 4: RATING_EASY}
        if n in mapping:
            self._answer(mapping[n])

    # ================================================================
    def _render_home(self):
        self.session_active = False
        for ch in self.sf.inner.winfo_children():
            ch.destroy()

        stats = storage.srs_stats()
        due = storage.srs_due()
        known = storage.srs_total_known()
        streak = storage.get("streak_days", 0)

        # Сводка
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))
        tk.Label(card, text="📊 " + self.t("srs_title"),
                 font=theme.font("h3"), bg=theme.c("card"),
                 fg=theme.c("accent"), anchor="w",
                 padx=20, pady=14).pack(fill="x")

        rows = [
            ("⏰ " + self.t("srs_due_now"), str(len(due))),
            ("🔥 Streak",                   f"{streak} дней" if streak else "0"),
            ("✅ " + self.t("srs_known"),   str(known)),
        ]
        for label, value in rows:
            r = tk.Frame(card, bg=theme.c("card"))
            r.pack(fill="x", padx=20, pady=2)
            tk.Label(r, text=label, font=theme.font("body"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     anchor="w", width=24).pack(side="left")
            tk.Label(r, text=value, font=theme.font("body_bold"),
                     bg=theme.c("card"), fg=theme.c("text"),
                     anchor="w").pack(side="left")
        tk.Frame(card, bg=theme.c("card"), height=12).pack()

        # Состояния карточек
        self._render_states(stats)

        # Распределение интервалов
        self._render_intervals()

    def _render_states(self, stats):
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))
        tk.Label(card, text=self.t("srs_stat_header"),
                 font=theme.font("h3"), bg=theme.c("card"),
                 fg=theme.c("accent"), anchor="w",
                 padx=20, pady=14).pack(fill="x")

        grid = tk.Frame(card, bg=theme.c("card"))
        grid.pack(fill="x", padx=20, pady=(0, 14))

        items = [
            (self.t("srs_state_new"),      stats.get("new", 0),      "#DDDDDD"),
            (self.t("srs_state_learning"), stats.get("learning", 0), "#FFE082"),
            (self.t("srs_state_review"),   stats.get("review", 0),   theme.c("success_bg")),
            (self.t("srs_state_relearn"),  stats.get("relearning", 0), theme.c("error_bg")),
        ]
        for label, count, bg in items:
            cell = tk.Frame(grid, bg=bg,
                            highlightbackground=theme.c("border"),
                            highlightthickness=1)
            cell.pack(side="left", padx=4, fill="x", expand=True)
            tk.Label(cell, text=label, font=theme.font("muted"),
                     bg=bg, fg=theme.c("text"), pady=8).pack()
            tk.Label(cell, text=str(count), font=(theme.ui_family, 22, "bold"),
                     bg=bg, fg=theme.c("text")).pack(pady=(0, 8))

    def _render_intervals(self):
        buckets = storage.srs_interval_distribution()
        labels = [
            self.t("srs_iv_lt7"), self.t("srs_iv_lt30"),
            self.t("srs_iv_lt90"), self.t("srs_iv_lt180"), self.t("srs_iv_ge180"),
        ]
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))
        tk.Label(card, text=self.t("srs_stat_interval"),
                 font=theme.font("h3"), bg=theme.c("card"),
                 fg=theme.c("accent"), anchor="w",
                 padx=20, pady=14).pack(fill="x")

        grid = tk.Frame(card, bg=theme.c("card"))
        grid.pack(fill="x", padx=20, pady=(0, 14))
        max_v = max(buckets) or 1

        for lbl, n in zip(labels, buckets):
            col = tk.Frame(grid, bg=theme.c("card"))
            col.pack(side="left", padx=4, fill="x", expand=True)

            h = max(4, int(60 * n / max_v))
            bar = tk.Frame(col, bg=theme.c("accent"), height=h, width=40)
            bar.pack()
            bar.pack_propagate(False)

            tk.Label(col, text=str(n), font=theme.font("body_bold"),
                     bg=theme.c("card"), fg=theme.c("text"),
                     pady=2).pack()
            tk.Label(col, text=lbl, font=theme.font("muted"),
                     bg=theme.c("card"), fg=theme.c("text_muted")).pack()

        tk.Label(card, text=f"{self.t('srs_ease_avg')}: {storage.srs_ease_avg()}",
                 font=theme.font("muted"), bg=theme.c("card"),
                 fg=theme.c("text_muted")).pack(pady=(0, 12))

    # ================================================================
    def _start_session(self):
        by_hanzi = {w.hanzi: (u, i, w) for u, i, w in self.all_words}

        # Убеждаемся, что все слова есть в SRS
        for u, i, w in self.all_words:
            storage._ensure_card(w.hanzi)

        due = storage.srs_due()
        queue = [by_hanzi[hz] for hz in due if hz in by_hanzi]
        random.shuffle(queue)

        self.queue = queue[:SESSION_SIZE]
        self.total = len(self.queue)
        self.index = 0
        self.correct = 0
        self.flipped = False
        self.session_active = True

        if self.total == 0:
            self._render_home()
            return
        self._render_card()

    def _clear(self):
        for ch in self.sf.inner.winfo_children():
            ch.destroy()

    def _render_card(self):
        self._clear()
        self.flipped = False

        if self.index >= self.total:
            self._render_finish()
            return

        unit, lesson_idx, w = self.queue[self.index]
        self.current = (unit, lesson_idx, w)

        rec = storage.srs_get(w.hanzi) or {}
        state = rec.get("state", "new")
        state_label = {
            "new": self.t("srs_state_new"),
            "learning": self.t("srs_state_learning"),
            "review": self.t("srs_state_review"),
            "relearning": self.t("srs_state_relearn"),
        }.get(state, "")

        top = tk.Frame(self.sf.inner, bg=theme.c("bg"))
        top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text=f"{self.index + 1} / {self.total}",
                 font=theme.font("body"), bg=theme.c("bg"),
                 fg=theme.c("text_muted")).pack(side="left")
        tk.Label(top, text=state_label, font=theme.font("muted"),
                 bg=theme.c("bg"), fg=theme.c("text_muted")).pack(side="left", padx=12)
        tk.Label(top, text=f"✓ {self.correct}",
                 font=theme.font("body_bold"), bg=theme.c("bg"),
                 fg=theme.c("success")).pack(side="right")

        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=2)
        card.pack(fill="x", pady=(0, 14))

        tk.Label(card, text=w.hanzi, font=(theme.cjk_family, 84, "bold"),
                 bg=theme.c("card"), fg=theme.c("text"), pady=40).pack()

        self.pinyin_lbl = tk.Label(card, text="", font=theme.font("pinyin"),
                                   bg=theme.c("card"), fg=theme.c("accent"))
        self.pinyin_lbl.pack()

        self.trans_lbl = tk.Label(card, text="", font=theme.font("h3"),
                                  bg=theme.c("card"), fg=theme.c("text_muted"))
        self.trans_lbl.pack(pady=10)

        self.btn_bar = tk.Frame(self.sf.inner, bg=theme.c("bg"))
        self.btn_bar.pack(pady=10)

        self.show_btn = tk.Button(
            self.btn_bar, text=self.t("srs_show"),
            font=theme.font("h3"), bg=theme.c("accent"), fg="white",
            activebackground=theme.c("accent_dark"),
            relief="flat", padx=24, pady=12, cursor="hand2",
            command=self._reveal,
        )
        self.show_btn.pack()

        hint = tk.Label(self.sf.inner,
                        text=self.t("srs_hotkeys_hint"),
                        font=theme.font("muted"), bg=theme.c("bg"),
                        fg=theme.c("text_muted"))
        hint.pack(pady=(0, 8))

        audio_file = getattr(w, "audio", "") or ""
        if audio_file and audio.exists(unit, lesson_idx, audio_file):
            tk.Button(self.btn_bar, text="🔊", font=(theme.ui_family, 14),
                      bg=theme.c("bg"), fg=theme.c("accent"),
                      relief="flat", padx=10, cursor="hand2",
                      command=(lambda u=unit, i=lesson_idx, f=audio_file:
                               audio.play(audio.find(u, i, f))),
                      ).pack(pady=(6, 0))

    def _reveal(self):
        if self.flipped:
            return
        self.flipped = True
        unit, lesson_idx, w = self.current
        self.pinyin_lbl.config(text=w.pinyin)
        self.trans_lbl.config(text=w.translate(self.i18n.language))

        self.show_btn.pack_forget()

        row = tk.Frame(self.btn_bar, bg=theme.c("bg"))
        row.pack()

        for txt, rating, bg in [
            (self.t("srs_again"), RATING_AGAIN, theme.c("error")),
            (self.t("srs_hard"),  RATING_HARD,  "#EF6C00"),
            (self.t("srs_good"),  RATING_GOOD,  theme.c("success")),
            (self.t("srs_easy"),  RATING_EASY,  "#1565C0"),
        ]:
            tk.Button(row, text=txt, font=theme.font("h3"),
                      bg=bg, fg="white", activebackground=bg,
                      relief="flat", padx=14, pady=12, cursor="hand2",
                      command=lambda r=rating: self._answer(r),
                      ).pack(side="left", padx=3)

    def _answer(self, rating: int):
        unit, lesson_idx, w = self.current
        storage.srs_review(w.hanzi, rating)

        # Правильно = не Again
        correct = rating != RATING_AGAIN
        storage.record_word(w.hanzi, correct)
        if correct:
            self.correct += 1

        # Показать следующий интервал
        rec = storage.srs_get(w.hanzi) or {}
        due_iso = rec.get("due", "")
        info = _fmt_interval(due_iso)

        if info.startswith("min:"):
            n = info.split(":")[1]
            text = self.t("srs_next_min").replace("{n}", n)
        elif info.startswith("days:"):
            n = info.split(":")[1]
            text = self.t("srs_next_days").replace("{n}", n)
        else:
            text = self.t("srs_next_now")

        self._flash(text)
        self.after(700, self._advance)

    def _flash(self, text):
        lbl = tk.Label(self.sf.inner, text=text, font=theme.font("body_bold"),
                       bg=theme.c("info_bg"), fg=theme.c("info"),
                       padx=16, pady=8)
        lbl.pack(pady=6)
        self.after(600, lbl.destroy)

    def _advance(self):
        self.index += 1
        self._render_card()

    def _render_finish(self):
        self.session_active = False
        self._clear()

        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=30)
        tk.Label(card, text=self.t("srs_finish"),
                 font=theme.font("h2"), bg=theme.c("card"),
                 fg=theme.c("accent"), pady=20).pack()
        tk.Label(card, text=f"{self.correct} / {self.total}",
                 font=(theme.ui_family, 32, "bold"),
                 bg=theme.c("card"), fg=theme.c("text")).pack()
        tk.Label(card, text=self.t("srs_correct"),
                 font=theme.font("body"), bg=theme.c("card"),
                 fg=theme.c("text_muted"), pady=(0, 20)).pack()

        btns = tk.Frame(self.sf.inner, bg=theme.c("bg"))
        btns.pack(pady=10)
        tk.Button(btns, text=self.t("srs_another"),
                  font=theme.font("body"), bg=theme.c("accent"),
                  fg="white", relief="flat", padx=16, pady=8, cursor="hand2",
                  command=self._render_home).pack(side="left", padx=6)
        tk.Button(btns, text=self.t("back"),
                  font=theme.font("body"), bg=theme.c("card"),
                  fg=theme.c("text"), relief="flat", padx=16, pady=8,
                  cursor="hand2",
                  command=lambda: self.manager.show("main_menu"),
                  ).pack(side="left", padx=6)