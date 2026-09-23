# -*- coding: utf-8 -*-
"""Тепловая карта активности за год (в стиле GitHub)."""
from datetime import date, timedelta
import tkinter as tk
from ui.base_screen import BaseScreen
from ui.widgets.scrollable import ScrollableFrame
from core.theme import theme
from core.storage import storage


WEEKS = 53
CELL = 14
GAP = 3

MONTHS_SHORT = {
    "ru": ["янв", "фев", "мар", "апр", "май", "июн",
           "июл", "авг", "сен", "окт", "ноя", "дек"],
    "tk": ["ýan", "few", "mart", "apr", "maý", "iýun",
           "iýul", "awg", "sen", "okt", "noý", "dek"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}

WEEKDAYS_SHORT = {
    "ru": ["Пн", "", "Ср", "", "Пт", "", ""],
    "tk": ["Du", "", "Ça", "", "An", "", ""],
    "en": ["Mon", "", "Wed", "", "Fri", "", ""],
}

# 5 уровней интенсивности
LEVEL_COLORS = [
    "bg_soft",       # 0 — пусто
    "#C6E48B",       # 1 — 1-4
    "#7BC96F",       # 2 — 5-9
    "#239A3B",       # 3 — 10-19
    "#196127",       # 4 — 20+
]


class HeatmapScreen(BaseScreen):

    def _build(self):
        self.make_header(self.t("heatmap_title"), back_to="main_menu")

        top = tk.Frame(self, bg=theme.c("bg"))
        top.pack(fill="x", padx=24, pady=(0, 8))
        tk.Button(top, text="🔄", font=theme.font("body"),
                  bg=theme.c("card"), fg=theme.c("accent_dark"),
                  activebackground=theme.c("accent_soft"),
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._refresh).pack(side="right")

        self.sf = ScrollableFrame(self)
        self.sf.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self._render()

    def _refresh(self):
        for ch in self.sf.inner.winfo_children():
            ch.destroy()
        self._render()

    # ================================================================
    def _level(self, count: int) -> int:
        if count <= 0:
            return 0
        if count < 5:
            return 1
        if count < 10:
            return 2
        if count < 20:
            return 3
        return 4

    def _render(self):
        activity = storage.get("activity", {}) or {}

        # --- Диапазон дат: последние 53 недели с выравниванием по Пн ---
        today = date.today()
        # Понедельник текущей недели:
        monday_this_week = today - timedelta(days=today.weekday())
        # Первая колонка = 52 недели назад от текущего понедельника
        start = monday_this_week - timedelta(weeks=WEEKS - 1)

        # Соберём данные в матрицу [col][row] = count
        grid_data = [[0] * 7 for _ in range(WEEKS)]
        max_count = 0
        total = 0
        active_days = 0
        best_day = (None, 0)

        for w in range(WEEKS):
            for d in range(7):
                cur = start + timedelta(weeks=w, days=d)
                if cur > today:
                    continue
                key = cur.isoformat()
                cnt = activity.get(key, 0)
                grid_data[w][d] = cnt
                total += cnt
                if cnt > 0:
                    active_days += 1
                if cnt > best_day[1]:
                    best_day = (key, cnt)
                if cnt > max_count:
                    max_count = cnt

        # --- Карточка с сеткой ---
        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        header = tk.Frame(card, bg=theme.c("card"))
        header.pack(fill="x", padx=20, pady=(14, 4))
        tk.Label(header, text=self.t("heatmap_title"),
                 font=theme.font("h3"), bg=theme.c("card"),
                 fg=theme.c("accent"), anchor="w").pack(side="left")

        # Контейнер с сеткой — используем Canvas + Frame
        grid_wrap = tk.Frame(card, bg=theme.c("card"))
        grid_wrap.pack(fill="x", padx=20, pady=(4, 8))

        # Метки месяцев сверху
        month_row = tk.Frame(grid_wrap, bg=theme.c("card"))
        month_row.pack(anchor="w", padx=(28, 0))  # отступ под метки дней

        months_labels = MONTHS_SHORT.get(self.i18n.language, MONTHS_SHORT["en"])
        cur_month = -1
        for w in range(WEEKS):
            col_date = start + timedelta(weeks=w)
            m = col_date.month
            if m != cur_month:
                cur_month = m
                lbl = tk.Label(month_row, text=months_labels[m - 1],
                               font=theme.font("muted"),
                               bg=theme.c("card"), fg=theme.c("text_muted"),
                               width=3, anchor="w")
                lbl.pack(side="left")
            else:
                tk.Frame(month_row, bg=theme.c("card"),
                         width=CELL + GAP, height=14).pack(side="left")

        # Строки: слева дни недели, справа — квадратики недель
        body = tk.Frame(grid_wrap, bg=theme.c("card"))
        body.pack(anchor="w")

        # Левая колонка с днями недели
        day_col = tk.Frame(body, bg=theme.c("card"))
        day_col.pack(side="left", padx=(0, 4))

        wd_labels = WEEKDAYS_SHORT.get(self.i18n.language, WEEKDAYS_SHORT["en"])
        for d in range(7):
            tk.Label(day_col, text=wd_labels[d],
                     font=theme.font("muted"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     width=3, anchor="e",
                     height=1).pack(pady=1)

        # Основная сетка — по колонкам
        cols_frame = tk.Frame(body, bg=theme.c("card"))
        cols_frame.pack(side="left")

        for w in range(WEEKS):
            col = tk.Frame(cols_frame, bg=theme.c("card"))
            col.pack(side="left", padx=(0, GAP))
            for d in range(7):
                cur = start + timedelta(weeks=w, days=d)
                if cur > today:
                    cell_bg = theme.c("card")
                else:
                    cnt = grid_data[w][d]
                    lvl = self._level(cnt)
                    cell_bg = theme.c(LEVEL_COLORS[lvl])
                cell = tk.Frame(col, bg=cell_bg, width=CELL, height=CELL,
                                highlightbackground=theme.c("border"),
                                highlightthickness=1)
                cell.pack(pady=(0, GAP))
                cell.pack_propagate(False)

                # Наведение — всплывающая подсказка
                self._attach_tooltip(cell, cur, grid_data[w][d])

        # Легенда
        legend = tk.Frame(card, bg=theme.c("card"))
        legend.pack(fill="x", padx=20, pady=(4, 14))
        tk.Label(legend, text=self.t("heatmap_less"),
                 font=theme.font("muted"), bg=theme.c("card"),
                 fg=theme.c("text_muted")).pack(side="left")
        for lvl in range(5):
            cell = tk.Frame(legend, bg=theme.c(LEVEL_COLORS[lvl]),
                            width=12, height=12,
                            highlightbackground=theme.c("border"),
                            highlightthickness=1)
            cell.pack(side="left", padx=2, pady=4)
            cell.pack_propagate(False)
        tk.Label(legend, text=self.t("heatmap_more"),
                 font=theme.font("muted"), bg=theme.c("card"),
                 fg=theme.c("text_muted")).pack(side="left")

        # --- Сводка ---
        self._render_summary(total, active_days, max_count, best_day)

    # ----------------------------------------------------------------
    def _attach_tooltip(self, widget, day: date, count: int):
        tip = {"win": None}

        def show(_e):
            if tip["win"]:
                return
            txt = f"{day.isoformat()}  ·  {count} {self.t('heatmap_cards')}"
            win = tk.Toplevel(widget)
            win.wm_overrideredirect(True)
            win.wm_geometry(f"+{widget.winfo_rootx() + 20}+{widget.winfo_rooty() - 30}")
            tk.Label(win, text=txt, font=theme.font("muted"),
                     bg="#333333", fg="white",
                     padx=8, pady=4).pack()
            tip["win"] = win

        def hide(_e):
            if tip["win"]:
                tip["win"].destroy()
                tip["win"] = None

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)

    # ----------------------------------------------------------------
    def _render_summary(self, total, active_days, max_count, best_day):
        streak = storage.get("streak_days", 0)

        card = tk.Frame(self.sf.inner, bg=theme.c("card"),
                        highlightbackground=theme.c("border"),
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="📈 " + self.t("stats_summary"),
                 font=theme.font("h3"), bg=theme.c("card"),
                 fg=theme.c("accent"), anchor="w",
                 padx=20, pady=14).pack(fill="x")

        best_txt = f"{best_day[1]} ({best_day[0]})" if best_day[0] else "—"
        avg = round(total / 365, 1) if total else 0

        rows = [
            (self.t("heatmap_streak"), f"{streak} {self.t('heatmap_days')}"),
            (self.t("heatmap_best"),   best_txt),
            (self.t("heatmap_total"),  f"{total} ({active_days} {self.t('heatmap_active')})"),
            (self.t("heatmap_avg"),    str(avg)),
        ]
        for label, value in rows:
            r = tk.Frame(card, bg=theme.c("card"))
            r.pack(fill="x", padx=20, pady=2)
            tk.Label(r, text=label, font=theme.font("body"),
                     bg=theme.c("card"), fg=theme.c("text_muted"),
                     anchor="w", width=26).pack(side="left")
            tk.Label(r, text=value, font=theme.font("body_bold"),
                     bg=theme.c("card"), fg=theme.c("text"),
                     anchor="w").pack(side="left")
        tk.Frame(card, bg=theme.c("card"), height=12).pack()