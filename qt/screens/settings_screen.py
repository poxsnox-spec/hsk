# -*- coding: utf-8 -*-
"""Полный экран настроек с профилем."""
import json
from datetime import datetime
from pathlib import Path

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFileDialog, QMessageBox, QFrame,
                             QLineEdit, QDialog, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QFont

from qt.theme import qt_theme
from qt.widgets import (OpaqueScrollPage, BackButton, scroll_bg_color,
                        primary_btn_qss, GlassCard)
from qt.icons import get_icon_font, icon
from qt.screens.profile_dialogs import ProfileSwitcherDialog
from core.i18n import i18n
from core.storage import storage
from core.profiles import profiles, COLOR_HEX
from core.config import PROGRESS_FILE, USER_DATA_DIR


ACCENT_COLORS = {
    "blue":   ("#66B2FF", "#4A8FCC"),
    "green":  ("#5CD68E", "#3AA86A"),
    "orange": ("#FFB84D", "#CC8A2A"),
    "purple": ("#B58EFF", "#8A66D6"),
}


def _group_card(title_text):
    s = qt_theme.scale
    card = GlassCard()
    lay = QVBoxLayout(card)
    lay.setContentsMargins(int(22 * s), int(16 * s),
                           int(22 * s), int(16 * s))
    lay.setSpacing(int(12 * s))

    title = QLabel(title_text)
    title.setFont(qt_theme.font("h3"))
    title.setStyleSheet(
        f"color: {qt_theme.c('accent')}; background: transparent;")
    lay.addWidget(title)
    return card, lay


def _row_label(text):
    lbl = QLabel(text)
    lbl.setFont(qt_theme.font("body"))
    lbl.setStyleSheet(
        f"color: {qt_theme.c('text_muted')}; background: transparent;")
    return lbl


def _value_label(text):
    lbl = QLabel(text)
    lbl.setFont(qt_theme.font("body_bold"))
    lbl.setStyleSheet(
        f"color: {qt_theme.c('text')}; background: transparent;")
    return lbl


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(i18n.t("help_title"))
        self.resize(700, 600)
        self.setStyleSheet(f"background-color: {scroll_bg_color()};")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setPlainText(i18n.t("help_text"))
        txt.setFont(QFont(qt_theme._ui, 11))
        txt.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(30, 46, 62, 240);
                color: {qt_theme.c('text')};
                border: 1px solid rgba(120, 160, 200, 80);
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        lay.addWidget(txt)

        close_btn = QPushButton(i18n.t("help_close"))
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setMinimumHeight(40)
        close_btn.setStyleSheet(primary_btn_qss())
        close_btn.clicked.connect(self.accept)
        lay.addWidget(close_btn)


class SettingsScreen(QWidget):
    back_requested = pyqtSignal()
    lang_changed = pyqtSignal()
    profile_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(scroll_bg_color()))
        self.setPalette(pal)

        if storage.get("profile_started") is None:
            storage.set("profile_started", datetime.now().isoformat())

        self._build()

    def _build(self):
        s = qt_theme.scale
        root = QVBoxLayout(self)
        root.setContentsMargins(int(40 * s), int(28 * s),
                                int(40 * s), int(28 * s))
        root.setSpacing(int(14 * s))

        top = QHBoxLayout()
        top.setSpacing(int(14 * s))
        back = BackButton(i18n.t("back_btn"))
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)

        title = QLabel(i18n.t("menu_settings_new"))
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        top.addWidget(title)
        top.addStretch()
        root.addLayout(top)

        scroll = OpaqueScrollPage()
        root.addWidget(scroll, 1)

        # === Новая крутая карточка профиля ===
        scroll.lay.addWidget(self._make_profile_card())
        scroll.lay.addWidget(self._make_dashboard_card())
        scroll.lay.addWidget(self._make_lang_card())
        scroll.lay.addWidget(self._make_srs_card())
        scroll.lay.addWidget(self._make_audio_card())
        scroll.lay.addWidget(self._make_accent_card())
        scroll.lay.addWidget(self._make_backup_card())
        scroll.lay.addWidget(self._make_actions_card())
        scroll.lay.addStretch()

    # ============================================================
    # 👤 Карточка профиля — как в проф. приложениях
    # ============================================================
    def _make_profile_card(self):
        s = qt_theme.scale
        p = profiles.get_active()
        if not p:
            return QWidget()

        card = GlassCard()
        lay = QVBoxLayout(card)
        lay.setContentsMargins(int(24 * s), int(20 * s),
                               int(24 * s), int(20 * s))
        lay.setSpacing(int(16 * s))

        # ---- Шапка: большой аватар + имя + кнопка управления ----
        head = QHBoxLayout()
        head.setSpacing(int(18 * s))

        # Аватар
        color, border = COLOR_HEX.get(p["color"], COLOR_HEX["blue"])
        av = QFrame()
        av.setFixedSize(int(84 * s), int(84 * s))
        av.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 2px solid {border};
                border-radius: {int(22 * s)}px;
            }}
        """)
        av_lay = QVBoxLayout(av)
        av_lay.setContentsMargins(0, 0, 0, 0)
        av_lbl = QLabel(p["avatar"])
        av_lbl.setFont(QFont("Segoe UI Emoji", int(44 * s)))
        av_lbl.setAlignment(Qt.AlignCenter)
        av_lbl.setStyleSheet("background: transparent;")
        av_lay.addWidget(av_lbl)
        head.addWidget(av)

        # Имя + мета
        text_box = QVBoxLayout()
        text_box.setSpacing(int(4 * s))

        name_lbl = QLabel(p["name"])
        f = qt_theme.font("h1")
        f.setPointSize(int(22 * s))
        name_lbl.setFont(f)
        name_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        text_box.addWidget(name_lbl)

        # Мета: дата создания + ид профиля
        try:
            created = datetime.fromisoformat(p.get("created", ""))
            cstr = created.strftime("%d.%m.%Y")
        except Exception:
            cstr = "—"
        meta_lbl = QLabel(f"📅 Учится с {cstr}  ·  ID: {p['id']}")
        meta_lbl.setFont(qt_theme.font("muted"))
        meta_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        text_box.addWidget(meta_lbl)

        head.addLayout(text_box, 1)

        # Кнопка "Сменить"
        switch_btn = QPushButton("🔄  " + i18n.t("profile_switch"))
        switch_btn.setCursor(Qt.PointingHandCursor)
        switch_btn.setMinimumHeight(int(44 * s))
        switch_btn.setStyleSheet(primary_btn_qss("rgba(74, 158, 255, 160)"))
        switch_btn.clicked.connect(self._open_profile_switcher)
        head.addWidget(switch_btn)

        lay.addLayout(head)

        # ---- Разделитель ----
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("QFrame { background-color: rgba(120, 160, 200, 60); }")
        lay.addWidget(div)

        # ---- Метрики профиля в ряд ----
        metrics = QHBoxLayout()
        metrics.setSpacing(int(10 * s))

        completed = len(storage.get("completed_lessons", []) or [])
        vocab = len(storage.get("vocab_stats", {}) or {})
        streak = storage.get("streak_days", 0)
        srs_cards = len(storage.get("srs", {}) or {})

        for label, value in [
            ("📚 Уроки",   f"{completed}/18"),
            ("💬 Слова",   str(vocab)),
            ("🔥 Streak",  f"{streak} дн."),
            ("🔁 SRS",     str(srs_cards)),
        ]:
            m_card = QFrame()
            m_card.setStyleSheet(f"""
                QFrame {{
                    background-color: rgba(30, 46, 62, 160);
                    border: 1px solid rgba(120, 160, 200, 50);
                    border-radius: {int(12 * s)}px;
                }}
            """)
            ml = QVBoxLayout(m_card)
            ml.setContentsMargins(int(12 * s), int(8 * s),
                                  int(12 * s), int(8 * s))
            ml.setSpacing(2)

            v_lbl = QLabel(value)
            fv = qt_theme.font("h3")
            v_lbl.setFont(fv)
            v_lbl.setAlignment(Qt.AlignCenter)
            v_lbl.setStyleSheet(
                f"color: {qt_theme.c('text')}; background: transparent;")
            ml.addWidget(v_lbl)

            l_lbl = QLabel(label)
            l_lbl.setFont(qt_theme.font("muted"))
            l_lbl.setAlignment(Qt.AlignCenter)
            l_lbl.setStyleSheet(
                f"color: {qt_theme.c('text_muted')}; background: transparent;")
            ml.addWidget(l_lbl)

            metrics.addWidget(m_card, 1)

        lay.addLayout(metrics)

        return card

    def _open_profile_switcher(self):
        dlg = ProfileSwitcherDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self.profile_changed.emit()
            self.lang_changed.emit()   # пересобрать экран

    # ============================================================
    def _make_dashboard_card(self):
        card, lay = _group_card(i18n.t("settings_dashboard"))
        completed = storage.get("completed_lessons", []) or []
        vocab = storage.get("vocab_stats", {}) or {}
        streak = storage.get("streak_days", 0)
        srs = storage.get("srs", {}) or {}

        rows = [
            (i18n.t("settings_lessons_done"), f"{len(completed)} / 18"),
            (i18n.t("settings_words_studied"), str(len(vocab))),
            (i18n.t("settings_streak"), str(streak)),
            (i18n.t("settings_srs_cards"), str(len(srs))),
        ]
        for k, v in rows:
            r = QHBoxLayout()
            r.addWidget(_row_label(k))
            r.addStretch()
            r.addWidget(_value_label(v))
            lay.addLayout(r)
        return card

    # ============================================================
    def _make_lang_card(self):
        s = qt_theme.scale
        card, lay = _group_card("🌐  " + i18n.t("change_lang"))
        row = QHBoxLayout()
        row.setSpacing(int(10 * s))
        for code, name in (("ru", "Русский"), ("tk", "Türkmençe"),
                            ("en", "English"), ("uz", "O'zbekcha"),
                            ("tg", "Тоҷикӣ")):
            active = i18n.language == code
            color = ("rgba(74, 158, 255, 160)" if active
                     else "rgba(40, 60, 84, 160)")
            b = QPushButton(name)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(int(46 * s))
            b.setStyleSheet(primary_btn_qss(color))
            b.clicked.connect(lambda _c=False, c=code: self._pick_lang(c))
            row.addWidget(b)
        row.addStretch()
        lay.addLayout(row)
        return card

    def _make_srs_card(self):
        s = qt_theme.scale
        card, lay = _group_card(i18n.t("settings_srs"))

        row = QHBoxLayout()
        row.setSpacing(int(8 * s))
        row.addWidget(_row_label(i18n.t("settings_session_size") + ":"))
        row.addStretch()
        cur_size = storage.get("srs_session_size", 20)
        for size in (10, 20, 30, 50):
            active = (size == cur_size)
            color = ("rgba(77, 212, 200, 180)" if active
                     else "rgba(40, 60, 84, 160)")
            b = QPushButton(str(size))
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedSize(int(60 * s), int(40 * s))
            b.setStyleSheet(primary_btn_qss(color))
            b.clicked.connect(lambda _c=False, sz=size:
                              self._set_setting("srs_session_size", sz, refresh=True))
            row.addWidget(b)
        lay.addLayout(row)

        row2 = QHBoxLayout()
        row2.setSpacing(int(8 * s))
        row2.addWidget(_row_label(i18n.t("settings_new_limit") + ":"))
        row2.addStretch()
        cur_limit = storage.get("srs_new_limit", 10)
        for val, label in [(5, "5"), (10, "10"), (20, "20"),
                            (999, i18n.t("settings_unlimited"))]:
            active = (val == cur_limit)
            color = ("rgba(77, 212, 200, 180)" if active
                     else "rgba(40, 60, 84, 160)")
            b = QPushButton(label)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(int(40 * s))
            b.setStyleSheet(primary_btn_qss(color))
            b.clicked.connect(lambda _c=False, v=val:
                              self._set_setting("srs_new_limit", v, refresh=True))
            row2.addWidget(b)
        lay.addLayout(row2)
        return card

    def _make_audio_card(self):
        s = qt_theme.scale
        card, lay = _group_card(i18n.t("settings_audio"))
        row = QHBoxLayout()
        row.setSpacing(int(10 * s))
        is_on = storage.get("sound_enabled", True)
        for val, label in [(True, i18n.t("settings_sound_on")),
                            (False, i18n.t("settings_sound_off"))]:
            active = (val == is_on)
            color = ("rgba(92, 214, 142, 180)" if active
                     else "rgba(40, 60, 84, 160)")
            b = QPushButton(label)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(int(46 * s))
            b.setStyleSheet(primary_btn_qss(color))
            b.clicked.connect(lambda _c=False, v=val:
                              self._set_setting("sound_enabled", v, refresh=False))
            row.addWidget(b)
        row.addStretch()
        lay.addLayout(row)
        return card

    def _make_accent_card(self):
        s = qt_theme.scale
        card, lay = _group_card(i18n.t("settings_appearance") + " · "
                                + i18n.t("settings_accent"))
        row = QHBoxLayout()
        row.setSpacing(int(10 * s))
        cur = storage.get("accent_color", "blue")
        for name, (color, dark) in ACCENT_COLORS.items():
            active = (name == cur)
            border = ("3px solid #FFFFFF" if active
                      else "1px solid rgba(255,255,255,60)")
            b = QPushButton()
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedSize(int(52 * s), int(52 * s))
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: {border};
                    border-radius: {int(14 * s)}px;
                }}
                QPushButton:hover {{
                    border: 3px solid rgba(255,255,255,180);
                }}
            """)
            b.clicked.connect(lambda _c=False, n=name:
                              self._set_setting("accent_color", n, refresh=True))
            row.addWidget(b)
        row.addStretch()
        lay.addLayout(row)
        return card

    def _make_backup_card(self):
        s = qt_theme.scale
        card, lay = _group_card(i18n.t("backup_section"))
        hint = QLabel(i18n.t("backup_hint"))
        hint.setWordWrap(True)
        hint.setFont(qt_theme.font("muted"))
        hint.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        lay.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(int(10 * s))
        export_btn = QPushButton(i18n.t("backup_export"))
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setMinimumHeight(int(46 * s))
        export_btn.setStyleSheet(primary_btn_qss("rgba(92, 214, 142, 160)"))
        export_btn.clicked.connect(self._export_progress)
        row.addWidget(export_btn)

        import_btn = QPushButton(i18n.t("backup_import"))
        import_btn.setCursor(Qt.PointingHandCursor)
        import_btn.setMinimumHeight(int(46 * s))
        import_btn.setStyleSheet(primary_btn_qss("rgba(74, 158, 255, 160)"))
        import_btn.clicked.connect(self._import_progress)
        row.addWidget(import_btn)
        row.addStretch()
        lay.addLayout(row)
        return card

    def _make_actions_card(self):
        s = qt_theme.scale
        card, lay = _group_card("⚙  Действия")

        row = QHBoxLayout()
        row.setSpacing(int(10 * s))

        help_btn = QPushButton(i18n.t("settings_help"))
        help_btn.setCursor(Qt.PointingHandCursor)
        help_btn.setMinimumHeight(int(48 * s))
        help_btn.setStyleSheet(primary_btn_qss("rgba(74, 158, 255, 160)"))
        help_btn.clicked.connect(self._show_help)
        row.addWidget(help_btn)

        about_btn = QPushButton(i18n.t("settings_about"))
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.setMinimumHeight(int(48 * s))
        about_btn.setStyleSheet(primary_btn_qss("rgba(120, 120, 200, 160)"))
        about_btn.clicked.connect(self._show_about)
        row.addWidget(about_btn)

        reset_btn = QPushButton(i18n.t("settings_reset"))
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.setMinimumHeight(int(48 * s))
        reset_btn.setStyleSheet(primary_btn_qss("rgba(255, 120, 120, 160)"))
        reset_btn.clicked.connect(self._reset_progress)
        row.addWidget(reset_btn)
        row.addStretch()
        lay.addLayout(row)

        quit_row = QHBoxLayout()
        quit_btn = QPushButton(i18n.t("settings_quit"))
        quit_btn.setCursor(Qt.PointingHandCursor)
        quit_btn.setMinimumHeight(int(48 * s))
        quit_btn.setStyleSheet(primary_btn_qss("rgba(180, 60, 60, 180)"))
        quit_btn.clicked.connect(self._quit_app)
        quit_row.addWidget(quit_btn)
        quit_row.addStretch()
        lay.addLayout(quit_row)
        return card

    # ============================================================
    def _set_setting(self, key, value, refresh=False):
        storage.set(key, value)
        if refresh:
            self.lang_changed.emit()

    def _pick_lang(self, code):
        i18n.set_language(code)
        storage.set("language", code)
        self.lang_changed.emit()

    def _show_help(self):
        HelpDialog(self).exec_()

    def _show_about(self):
        from core.config import APP_NAME, APP_VERSION
        QMessageBox.about(
            self, i18n.t("settings_about"),
            f"<h3>{APP_NAME} v{APP_VERSION}</h3>"
            "<p>Тренажёр по учебнику <b>HSK 5 上</b>.</p>"
            "<p>Учебник: 姜丽萍 (ed.), 北京语言大学出版社, 2015.</p>"
            "<p>PyQt5 · Liquid Glass · 3 languages</p>"
        )

    def _reset_progress(self):
        r = QMessageBox.question(self, "⚠",
                                  i18n.t("settings_reset_warn"),
                                  QMessageBox.Yes | QMessageBox.No)
        if r != QMessageBox.Yes:
            return
        keep = {
            "language": storage.get("language", "ru"),
            "profile_name": storage.get("profile_name", ""),
            "profile_started": storage.get("profile_started"),
            "theme_mode": "glass",
        }
        storage._data = storage._default()
        for k, v in keep.items():
            storage._data[k] = v
        storage.save()
        QMessageBox.information(self, "✓", i18n.t("settings_reset_done"))
        self.lang_changed.emit()

    def _quit_app(self):
        r = QMessageBox.question(self, "⚠",
                                  i18n.t("settings_quit_warn"),
                                  QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()

    def _export_progress(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default = f"hsk5_backup_{timestamp}.json"
        path, _ = QFileDialog.getSaveFileName(
            self, i18n.t("backup_export"),
            str(Path.home() / default), "JSON (*.json)")
        if not path:
            return
        try:
            backup = {
                "app": "HSK 5 Learner",
                "version": 1,
                "exported_at": timestamp,
                "data": storage._data,
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(backup, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, i18n.t("backup_export"),
                                     f"{i18n.t('backup_export_ok')}:\n\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def _import_progress(self):
        path, _ = QFileDialog.getOpenFileName(
            self, i18n.t("backup_import"),
            str(Path.home()), "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "data" in data and "app" in data:
                payload = data["data"]
            elif "language" in data or "srs" in data:
                payload = data
            else:
                raise ValueError("unknown format")
            storage._data = payload
            storage.save()
            if "language" in payload:
                i18n.set_language(payload["language"])
            QMessageBox.information(self, i18n.t("backup_import"),
                                     i18n.t("backup_import_ok"))
            self.lang_changed.emit()
        except Exception as e:
            QMessageBox.warning(self, i18n.t("backup_import"),
                                 f"{i18n.t('backup_import_warn')}\n\n{e}")
