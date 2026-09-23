# -*- coding: utf-8 -*-
"""Словарь: динамические колонки — только текущий язык интерфейса."""
import csv

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QLineEdit, QComboBox,
                             QTableView, QHeaderView, QAbstractItemView,
                             QMessageBox)
from PyQt5.QtCore import (Qt, pyqtSignal, QAbstractTableModel, QModelIndex,
                          QVariant, QSortFilterProxyModel)
from PyQt5.QtGui import QColor, QFont, QPalette

from qt.theme import qt_theme
from qt.icons import get_icon_font, icon
from qt.widgets import scroll_bg_color, primary_btn_qss, back_btn_qss
from core.i18n import i18n
from core.config import USER_DATA_DIR
from core.audio import audio
from core.storage import storage
from models.lesson import load_lesson


# Цвета юнитов
UNIT_COLORS = {
    1: "#3A6088",
    2: "#3A7060",
    3: "#7A6030",
    4: "#5A4A88",
    5: "#3A7080",
    6: "#7A3A60",
}


# Динамические колонки: lesson + hanzi + pinyin + pos + <язык>
def get_columns():
    """Возвращает список ключей колонок для текущего языка."""
    cur_lang = i18n.language
    return ["lesson", "hanzi", "pinyin", "pos", cur_lang]


def get_headers():
    """Возвращает заголовки колонок для текущего языка."""
    cur_lang = i18n.language
    lang_label = {"ru": "RU", "tk": "TK", "en": "EN"}.get(cur_lang, "EN")
    return [
        i18n.t("vocab_lesson_col"),
        i18n.t("vocab_col_hanzi"),
        i18n.t("vocab_col_pinyin"),
        i18n.t("vocab_col_pos"),
        lang_label,
    ]


class VocabModel(QAbstractTableModel):
    def __init__(self, words):
        super().__init__()
        self._words = words
        self._cols = get_columns()

    def rowCount(self, parent=QModelIndex()):
        return len(self._words)

    def columnCount(self, parent=QModelIndex()):
        return len(self._cols)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        row = index.row()
        col = index.column()
        if row >= len(self._words) or col >= len(self._cols):
            return QVariant()
        item = self._words[row]
        w = item["w"]
        key = self._cols[col]

        if role == Qt.DisplayRole:
            if key == "lesson":
                return item["label"]
            if key == "hanzi":
                return w.hanzi
            if key == "pinyin":
                return w.pinyin
            if key == "pos":
                return w.pos
            return w.translate(key)   # ru/tk/en

        elif role == Qt.ForegroundRole:
            if key == "hanzi":
                return QColor(qt_theme.c("accent"))
            if key in ("pinyin", "pos"):
                return QColor(qt_theme.c("text_muted"))
            return QColor(qt_theme.c("text"))

        elif role == Qt.FontRole:
            if key == "hanzi":
                f = QFont(qt_theme._cjk)
                f.setPointSize(int(14 * qt_theme.scale))
                f.setBold(True)
                return f
            if key == "lesson":
                f = QFont(qt_theme._ui)
                f.setPointSize(int(11 * qt_theme.scale))
                f.setBold(True)
                return f
            return QVariant()

        elif role == Qt.BackgroundRole:
            if key == "lesson":
                return QColor(UNIT_COLORS.get(item["unit"], "#3A6088"))

        elif role == Qt.TextAlignmentRole:
            if key == "lesson":
                return int(Qt.AlignCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)

        elif role == Qt.ToolTipRole:
            # В подсказке показываем ВСЕ 3 языка — удобно
            return (f"Урок {item['label']}\n"
                    f"{w.hanzi}  ({w.pinyin})\n"
                    f"({w.pos})\n"
                    f"RU: {w.translate('ru')}\n"
                    f"TK: {w.translate('tk')}\n"
                    f"EN: {w.translate('en')}")

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation != Qt.Horizontal:
            return QVariant()
        headers = get_headers()
        if role == Qt.DisplayRole:
            if section < len(headers):
                return headers[section]
            return ""
        if role == Qt.ForegroundRole:
            return QColor(qt_theme.c("text"))
        if role == Qt.FontRole:
            f = QFont(qt_theme._ui)
            f.setPointSize(int(11 * qt_theme.scale))
            f.setBold(True)
            return f
        return QVariant()

    def get_item(self, row):
        if 0 <= row < len(self._words):
            return self._words[row]
        return None


class VocabProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self._query = ""
        self._lesson_filter = None

    def set_query(self, q):
        self._query = (q or "").strip().lower()
        self.invalidateFilter()

    def set_lesson_filter(self, label):
        self._lesson_filter = label
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        item = model.get_item(source_row)
        if item is None:
            return False
        if self._lesson_filter and item["label"] != self._lesson_filter:
            return False
        if self._query:
            w = item["w"]
            haystack = " ".join([
                item["label"], w.hanzi, w.pinyin, w.pos,
                w.translate("ru"), w.translate("tk"), w.translate("en"),
            ]).lower()
            if self._query not in haystack:
                return False
        return True


class VocabScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)

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

        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(32 * s), int(24 * s),
                                int(32 * s), int(24 * s))
        root.setSpacing(int(12 * s))

        # ============ ВЕРХНЯЯ ПАНЕЛЬ ============
        top = QHBoxLayout()
        top.setSpacing(int(14 * s))

        back = QPushButton()
        back.setCursor(Qt.PointingHandCursor)
        back.setFixedSize(int(110 * s), int(40 * s))
        back.setText(f"  {icon('chevron')}   {i18n.t('back_btn')}")
        back.setFont(get_icon_font(int(13 * s)))
        back.setStyleSheet(back_btn_qss())
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        title = QLabel(i18n.t("vocab_title"))
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        title_box.addWidget(title)

        self.sub_lbl = QLabel("")
        self.sub_lbl.setFont(qt_theme.font("muted"))
        self.sub_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        title_box.addWidget(self.sub_lbl)

        top.addLayout(title_box)
        top.addStretch()
        root.addLayout(top)

        # ============ ПАНЕЛЬ УПРАВЛЕНИЯ ============
        ctrl = QHBoxLayout()
        ctrl.setSpacing(int(10 * s))

        self.search = QLineEdit()
        self.search.setPlaceholderText(i18n.t("vocab_search_ph"))
        self.search.setMinimumHeight(int(40 * s))
        f = QFont(qt_theme._ui, int(12 * s))
        self.search.setFont(f)
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(30, 46, 62, 220);
                border: 1px solid rgba(120, 160, 200, 80);
                border-radius: 10px;
                padding: 6px 14px;
                color: {qt_theme.c('text')};
            }}
            QLineEdit:focus {{ border: 1px solid {qt_theme.c('accent')}; }}
        """)
        self.search.textChanged.connect(self._on_search)
        ctrl.addWidget(self.search, 1)

        self.filter = QComboBox()
        self.filter.setMinimumHeight(int(40 * s))
        self.filter.setMinimumWidth(int(160 * s))
        self.filter.setFont(f)
        self.filter.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(30, 46, 62, 220);
                border: 1px solid rgba(120, 160, 200, 80);
                border-radius: 10px;
                padding: 6px 14px;
                color: {qt_theme.c('text')};
            }}
            QComboBox::drop-down {{ border: none; width: 28px; }}
            QComboBox QAbstractItemView {{
                background-color: rgba(20, 34, 48, 250);
                border: 1px solid rgba(120, 160, 200, 80);
                color: {qt_theme.c('text')};
                selection-background-color: rgba(74, 158, 255, 120);
            }}
        """)
        self.filter.addItem(i18n.t("vocab_unit_filter"), None)
        labels = sorted({item["label"] for item in self.all_words},
                        key=self._sort_label)
        for lbl in labels:
            self.filter.addItem(lbl, lbl)
        self.filter.currentIndexChanged.connect(self._on_filter)
        ctrl.addWidget(self.filter)

        export_btn = QPushButton("📤  " + i18n.t("vocab_export"))
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setMinimumHeight(int(40 * s))
        export_btn.setStyleSheet(primary_btn_qss())
        export_btn.clicked.connect(self._export_csv)
        ctrl.addWidget(export_btn)

        root.addLayout(ctrl)

        # ============ ТАБЛИЦА ============
        self.model = VocabModel(self.all_words)
        self.proxy = VocabProxy()
        self.proxy.setSourceModel(self.model)

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(self._table_qss())

        hdr = self.table.horizontalHeader()
        hdr.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hdr.setStretchLastSection(True)

        # Настраиваем ширину под динамические колонки
        self.table.setColumnWidth(0, int(70 * s))   # lesson
        self.table.setColumnWidth(1, int(90 * s))   # hanzi
        self.table.setColumnWidth(2, int(140 * s))  # pinyin
        self.table.setColumnWidth(3, int(80 * s))   # pos
        hdr.setSectionResizeMode(4, QHeaderView.Stretch)   # язык

        self.table.doubleClicked.connect(self._on_double_click)
        root.addWidget(self.table, 1)

        # ============ СТАТУС ============
        status_row = QHBoxLayout()
        self.status = QLabel("")
        self.status.setFont(qt_theme.font("muted"))
        self.status.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        status_row.addWidget(self.status)
        status_row.addStretch()

        hint = QLabel("💡 " + i18n.t("vocab_hint"))
        hint.setFont(qt_theme.font("muted"))
        hint.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        status_row.addWidget(hint)
        root.addLayout(status_row)

        self._update_status()

    def _table_qss(self):
        return f"""
            QTableView {{
                background-color: rgba(20, 32, 46, 230);
                color: {qt_theme.c('text')};
                border: 1px solid rgba(120, 160, 200, 60);
                border-radius: 12px;
                gridline-color: transparent;
                selection-background-color: rgba(74, 158, 255, 100);
                selection-color: {qt_theme.c('text')};
                font-size: 11pt;
                padding: 6px;
            }}
            QTableView::item {{
                padding: 8px 10px;
                border: none;
                border-bottom: 1px solid rgba(120, 160, 200, 30);
            }}
            QTableView::item:selected {{
                background-color: rgba(74, 158, 255, 100);
            }}
            QHeaderView::section {{
                background-color: rgba(30, 46, 64, 240);
                color: {qt_theme.c('text')};
                padding: 10px;
                border: none;
                border-bottom: 1px solid rgba(140, 180, 220, 80);
                border-right: 1px solid rgba(120, 160, 200, 30);
                font-weight: bold;
            }}
            QHeaderView::section:hover {{
                background-color: rgba(50, 76, 104, 240);
            }}
            QScrollBar:vertical {{
                background: rgba(40, 60, 84, 140);
                width: 10px; border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(120, 160, 200, 170);
                border-radius: 5px; min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none; border: none;
            }}
        """

    def _sort_label(self, lbl):
        try:
            u, l = lbl.split(".")
            return (int(u), int(l))
        except Exception:
            return (99, 99)

    def _on_search(self, text):
        self.proxy.set_query(text)
        self._update_status()

    def _on_filter(self, idx):
        label = self.filter.itemData(idx)
        self.proxy.set_lesson_filter(label)
        self._update_status()

    def _update_status(self):
        total = self.model.rowCount()
        shown = self.proxy.rowCount()
        self.status.setText(
            f"{i18n.t('vocab_rows_found')}: {shown}   ·   "
            f"{i18n.t('vocab_rows_total')}: {total}"
        )
        self.sub_lbl.setText(f"{total} слов · 6 юнитов")

    def _on_double_click(self, index):
        source_index = self.proxy.mapToSource(index)
        item = self.model.get_item(source_index.row())
        if not item:
            return
        w = item["w"]
        af = getattr(w, "audio", "") or ""
        if af and audio.exists(item["unit"], item["index"], af):
            audio.play(audio.find(item["unit"], item["index"], af))

    def _export_csv(self):
        out = USER_DATA_DIR / "vocabulary.csv"
        try:
            with open(out, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Hanzi", "Pinyin", "POS",
                    "RU", "TK", "EN", "Lesson",
                ])
                for item in self.all_words:
                    w = item["w"]
                    writer.writerow([
                        w.hanzi, w.pinyin, w.pos,
                        w.translate("ru"), w.translate("tk"), w.translate("en"),
                        item["label"],
                    ])
            QMessageBox.information(
                self,
                i18n.t("vocab_export"),
                f"✅ {i18n.t('vocab_export_done')}:\n\n{out}\n\n"
                f"📊 Всего: {len(self.all_words)} слов"
            )
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))
