# -*- coding: utf-8 -*-
"""Экран со списком уроков, сгруппированных по юнитам."""
import tkinter as tk
from ui.base_screen import BaseScreen
from core.theme import theme
from core.config import UNIT_TITLES, LESSONS_PER_UNIT, TOTAL_UNITS
from core.storage import storage


LESSON_TITLES = {
    (1, 1): {
        "zh": "爱的细节",
        "ru": "Детали любви",
        "tk": "Söýginiň jikme-jiklikleri",
        "en": "Details of Love",
    },
    (1, 2): {
        "zh": "留串钥匙给父母",
        "ru": "Оставить связку ключей родителям",
        "tk": "Ene-ata bir desse açar galdyrmak",
        "en": "Leaving a Bunch of Keys",
    },
    (1, 3): {
        "zh": "人生有选择，一切可改变",
        "ru": "В жизни есть выбор — всё можно изменить",
        "tk": "Durmuşda saýlaw bar — hemme zat üýtgäp biler",
        "en": "Having Choices Makes Change",
    },
    (2, 1): {
        "zh": "子路背米",
        "ru": "Цзылу несёт рис",
        "tk": "Tszyly tüwi göterýär",
        "en": "Zilu Carrying Rice",
    },
    (2, 2): {
        "zh": "济南的泉水",
        "ru": "Источники Цзинаня",
        "tk": "Tszinan çeşmeleri",
        "en": "Spring Water in Ji'nan",
    },
    (2, 3): {
        "zh": "除夕的由来",
        "ru": "Происхождение Чуси",
        "tk": "Çusi baýramynyň gelip çykyşy",
        "en": "Origin of Chuxi",
    },
    (3, 1): {
        "zh": "成语故事两则",
        "ru": "Две истории об идиомах",
        "tk": "Iki idiom hekaýasy",
        "en": "Two Idiom Stories",
    },
    (3, 2): {
        "zh": "「朝三暮四」的古今义",
        "ru": "«Утром три, вечером четыре»",
        "tk": "«Irden üç, agşam dört»",
        "en": "Three at Dawn, Four at Dusk",
    },
    (3, 3): {
        "zh": "别样鲁迅",
        "ru": "Другой Лу Синь",
        "tk": "Başgaça Lu Sýun",
        "en": "The Lu Xun You Don't Know",
    },
    (4, 1): {
        "zh": "争论的奇迹",
        "ru": "Чудо спора",
        "tk": "Jedeliň gudraty",
        "en": "Miracle of Debate",
    },
    (4, 2): {
        "zh": "闹钟的危害",
        "ru": "Вред будильника",
        "tk": "Jaňly sagadyň zyýany",
        "en": "Harm of Alarm Clocks",
    },
    (4, 3): {
        "zh": "海外用户玩儿微信",
        "ru": "WeChat за рубежом",
        "tk": "Daşary ýurtda WeChat",
        "en": "Overseas Users of WeChat",
    },
    (5, 1): {
        "zh": "锯掉生活的「筐底」",
        "ru": "Отпилить «дно корзины»",
        "tk": "Durmuşyň «sebet düýbüni» kesmek",
        "en": "Cutting Off the 'Basket Bottom'",
    },
    (5, 2): {
        "zh": "北京的四合院",
        "ru": "Пекинские сыхэюани",
        "tk": "Pekiniň syheýuanlary",
        "en": "Beijing Quadrangle Courtyards",
    },
    (5, 3): {
        "zh": "纸上谈兵",
        "ru": "Битва на бумаге",
        "tk": "Kagyzda söweşmek",
        "en": "Armchair Strategist",
    },
    (6, 1): {
        "zh": "体重与节食",
        "ru": "Вес и диета",
        "tk": "Agram we iýmit çäklendirmesi",
        "en": "Weight and Diet",
    },
    (6, 2): {
        "zh": "在最美好的时刻离开",
        "ru": "Уйти в лучший момент",
        "tk": "Iň ajaýyp pursatda gitmek",
        "en": "Ending at the Best Moment",
    },
    (6, 3): {
        "zh": "抽象艺术美不美",
        "ru": "Красиво ли абстрактное искусство?",
        "tk": "Abstrakt sungat owadanmy?",
        "en": "Abstract Art: Beautiful or Not?",
    },
}


class LessonMenuScreen(BaseScreen):

    def _build(self):
        self.make_header(self.t("lessons_title"), back_to="main_menu")

        outer = tk.Frame(self, bg=theme.c("bg"))
        outer.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        canvas = tk.Canvas(outer, bg=theme.c("bg"), highlightthickness=0)
        scroll = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=theme.c("bg"))

        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

        for unit in range(1, TOTAL_UNITS + 1):
            self._render_unit(inner, unit)

    def _render_unit(self, parent, unit: int):
        head = tk.Frame(parent, bg=theme.c("bg"))
        head.pack(fill="x", pady=(18, 6), padx=4)

        title = UNIT_TITLES.get(unit, {})
        zh = title.get("zh", "")
        tr = title.get(self.i18n.language, title.get("en", ""))

        tk.Label(head, text=f"{self.t('unit')} {unit}",
                 font=theme.font("muted"), bg=theme.c("bg"),
                 fg=theme.c("accent")).pack(anchor="w")
        tk.Label(head, text=f"{zh}  ·  {tr}",
                 font=theme.font("h3"), bg=theme.c("bg"),
                 fg=theme.c("text")).pack(anchor="w")

        for idx in range(1, LESSONS_PER_UNIT + 1):
            self._render_lesson_row(parent, unit, idx)

    def _render_lesson_row(self, parent, unit: int, index: int):
        lesson_id = f"unit{unit}_lesson{index}"
        completed = lesson_id in storage.get("completed_lessons", [])

        titles = LESSON_TITLES.get((unit, index), {})
        zh = titles.get("zh", f"Урок {unit}.{index}")
        tr = titles.get(self.i18n.language, titles.get("ru", ""))

        row = tk.Frame(parent, bg=theme.c("card"),
                       highlightbackground=theme.c("border"),
                       highlightthickness=1, cursor="hand2")
        row.pack(fill="x", pady=3, padx=4)

        num = tk.Label(row, text=f"{unit}.{index}",
                       font=theme.font("h3"), bg=theme.c("card"),
                       fg=theme.c("accent"), width=4)
        num.pack(side="left", padx=(14, 8), pady=14)

        name_box = tk.Frame(row, bg=theme.c("card"))
        name_box.pack(side="left", fill="x", expand=True)
        tk.Label(name_box, text=zh, font=(theme.cjk_family, 16, "bold"),
                 bg=theme.c("card"), fg=theme.c("text"), anchor="w").pack(anchor="w")
        tk.Label(name_box, text=tr, font=theme.font("muted"),
                 bg=theme.c("card"), fg=theme.c("text_muted"), anchor="w").pack(anchor="w")

        if completed:
            tk.Label(row, text="✓", font=(theme.ui_family, 18, "bold"),
                     bg=theme.c("card"), fg=theme.c("success")).pack(side="right", padx=16)

        def _open(_e=None):
            self.manager.show("lesson_view", unit=unit, index=index)
        for w in (row, num, name_box, *name_box.winfo_children()):
            w.bind("<Button-1>", _open)