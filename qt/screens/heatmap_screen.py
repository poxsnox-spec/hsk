# -*- coding: utf-8 -*-
"""Активность за год — тепловая карта в стиле GitHub."""
from datetime import date, timedelta

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal

from qt.theme import qt_theme
from qt.widgets import ScrollPage, GlassCard, PageHeader
from core.i18n import i18n
from core.storage import storage


WEEKS = 53
LEVELS = [
    "rgba(40, 60, 84, 120)",     # 0 — пусто
    "rgba(92, 214, 142, 90)",    # 1 — 1-4
    "rgba(92, 214, 142, 150)",   # 2 — 5-9
    "rgba(92, 214, 142, 210)",   # 3 — 10-19
    "rgba(120, 235, 160, 255)",  # 4 — 20+
]

MONTHS = {
    "ru": ["янв", "фев", "мар", "апр", "май", "июн",
           "июл", "авг", "сен", "окт", "ноя", "дек"],
    "tk": ["ýan", "few", "mart", "apr", "maý", "iýun",
           "iýul", "awg", "sen", "okt", "noý", "dek"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}


def _level(cnt):
    if cnt <= 0: return 0
    if cnt < 5: return 1
    if cnt < 10: return 2
    if cnt < 20: return 3
    return 4


class HeatmapScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        header = PageHeader(i18n.t("heatmap_title"))
        header.back_clicked.connect(self.back_requested.emit)
        root.addWidget(header)

        content = ScrollPage(self)
        root.addWidget(content, 1)

        # Данные
        activity = storage.get("activity", {}) or {}
        today = date.today()
        monday_this_week = today - timedelta(days=today.weekday())
        start = monday_this_week - timedelta(weeks=WEEKS - 1)

        grid_data = [[0] * 7 for _ in range(WEEKS)]
        total = 0
        best = (None, 0)
        for w in range(WEEKS):
            for d in range(7):
                cur = start + timedelta(weeks=w, days=d)
                if cur > today:
                    continue
                cnt = activity.get(cur.isoformat(), 0)
                grid_data[w][d] = cnt
                total += cnt
                if cnt > best[1]:
                    best = (cur.isoformat(), cnt)

        # Карточка
        card = GlassCard()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(int(22 * s), int(18 * s),
                              int(22 * s), int(18 * s))
        cl.setSpacing(int(10 * s))

        title = QLabel(i18n.t("heatmap_title"))
        ft = qt_theme.font("h3")
        title.setFont(ft)
        title.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        cl.addWidget(title)

        # Сетка
        grid = QGridLayout()
        grid.setSpacing(int(3 * s))

        months_row = MONTHS.get(i18n.language, MONTHS["en"])
        cur_month = -1
        for w in range(WEEKS):
            col_date = start + timedelta(weeks=w)
            m = col_date.month
            if m != cur_month:
                cur_month = m
                lbl = QLabel(months_row[m - 1])
                lbl.setFont(qt_theme.font("muted"))
                lbl.setStyleSheet(
                    f"color: {qt_theme.c('text_muted')}; background: transparent;")
                grid.addWidget(lbl, 0, w + 1)

            for d in range(7):
                cur = start + timedelta(weeks=w, days=d)
                cnt = grid_data[w][d]
                if cur > today:
                    color = "transparent"
                else:
                    color = LEVELS[_level(cnt)]

                cell = QFrame()
                cell.setFixedSize(int(14 * s), int(14 * s))
                cell.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border-radius: {int(3 * s)}px;
                    }}
                """)
                if cur <= today:
                    cell.setToolTip(f"{cur.isoformat()}  ·  {cnt} карточек")
                grid.addWidget(cell, d + 1, w + 1)

        grid_w = QWidget()
        grid_w.setLayout(grid)
        cl.addWidget(grid_w)

        # Легенда
        legend = QHBoxLayout()
        legend.addWidget(QLabel(i18n.t("heatmap_less")))
        for lvl in range(5):
            cell = QFrame()
            cell.setFixedSize(int(14 * s), int(14 * s))
            cell.setStyleSheet(f"""
                QFrame {{
                    background-color: {LEVELS[lvl]};
                    border-radius: {int(3 * s)}px;
                }}
            """)
            legend.addWidget(cell)
        legend.addWidget(QLabel(i18n.t("heatmap_more")))
        legend.addStretch()
        legend_w = QWidget()
        legend_w.setLayout(legend)
        cl.addWidget(legend_w)

        content.lay.addWidget(card)

        # Сводка
        summary = GlassCard()
        sl = QVBoxLayout(summary)
        sl.setContentsMargins(int(22 * s), int(18 * s),
                              int(22 * s), int(18 * s))
        sl.setSpacing(int(8 * s))

        st = QLabel("📈 " + i18n.t("stats_summary"))
        st.setFont(qt_theme.font("h3"))
        st.setStyleSheet(
            f"color: {qt_theme.c('accent')}; background: transparent;")
        sl.addWidget(st)

        rows = [
            (i18n.t("heatmap_streak"), f"{storage.get('streak_days', 0)} дней"),
            (i18n.t("heatmap_best"),   f"{best[1]} ({best[0]})" if best[0] else "—"),
            (i18n.t("heatmap_total"),  str(total)),
        ]
        for k, v in rows:
            r = QHBoxLayout()
            kl = QLabel(k)
            kl.setFont(qt_theme.font("body"))
            kl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            r.addWidget(kl)
            r.addStretch()
            vl = QLabel(v)
            vl.setFont(qt_theme.font("body_bold"))
            vl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            r.addWidget(vl)
            w_r = QWidget()
            w_r.setLayout(r)
            sl.addWidget(w_r)

        content.lay.addWidget(summary)
        content.lay.addStretch()
