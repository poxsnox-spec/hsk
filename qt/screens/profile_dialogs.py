# -*- coding: utf-8 -*-
"""Диалоги профиля: смена, создание, редактирование."""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFrame, QMessageBox,
                             QScrollArea, QWidget, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPalette

from qt.theme import qt_theme
from qt.widgets import scroll_bg_color, primary_btn_qss
from qt.icons import get_icon_font
from core.i18n import i18n
from core.profiles import profiles, AVATARS, AVATAR_COLORS, COLOR_HEX


def _dialog_qss():
    return f"""
        QDialog {{
            background-color: {scroll_bg_color()};
        }}
        QLabel {{ color: {qt_theme.c('text')}; background: transparent; }}
        QLineEdit {{
            background-color: rgba(30, 46, 62, 220);
            border: 1px solid rgba(120, 160, 200, 80);
            border-radius: 10px;
            padding: 8px 14px;
            color: {qt_theme.c('text')};
            font-size: 12pt;
        }}
        QLineEdit:focus {{ border: 1px solid {qt_theme.c('accent')}; }}
    """


class ProfileCard(QFrame):
    """Карточка профиля в списке."""
    clicked = pyqtSignal(str)
    delete_requested = pyqtSignal(str)
    edit_requested = pyqtSignal(str)

    def __init__(self, profile, is_active=False, can_delete=False, parent=None):
        super().__init__(parent)
        s = qt_theme.scale
        self.profile = profile
        self.setObjectName("profileCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumHeight(int(76 * s))
        self.setCursor(Qt.PointingHandCursor)

        color, border = COLOR_HEX.get(profile["color"], COLOR_HEX["blue"])
        if is_active:
            self.setStyleSheet(f"""
                QFrame#profileCard {{
                    background-color: rgba(74, 158, 255, 100);
                    border: 2px solid {qt_theme.c('accent')};
                    border-radius: 14px;
                }}
                QFrame#profileCard QLabel {{ background: transparent; }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame#profileCard {{
                    background-color: rgba(30, 46, 62, 200);
                    border: 1px solid rgba(120, 160, 200, 60);
                    border-radius: 14px;
                }}
                QFrame#profileCard:hover {{
                    background-color: rgba(50, 76, 104, 220);
                    border: 1px solid rgba(140, 180, 220, 100);
                }}
                QFrame#profileCard QLabel {{ background: transparent; }}
            """)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(int(14 * s), int(10 * s),
                               int(14 * s), int(10 * s))
        lay.setSpacing(int(14 * s))

        # Аватар
        av = QFrame()
        av.setFixedSize(int(48 * s), int(48 * s))
        av.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 1px solid {border};
                border-radius: {int(14 * s)}px;
            }}
        """)
        av_lay = QVBoxLayout(av)
        av_lay.setContentsMargins(0, 0, 0, 0)
        av_lbl = QLabel(profile["avatar"])
        av_lbl.setFont(QFont("Segoe UI Emoji", int(24 * s)))
        av_lbl.setAlignment(Qt.AlignCenter)
        av_lbl.setStyleSheet("background: transparent;")
        av_lay.addWidget(av_lbl)
        lay.addWidget(av)

        # Имя
        text_box = QVBoxLayout()
        text_box.setSpacing(2)

        name_lbl = QLabel(profile["name"])
        f = qt_theme.font("h3")
        name_lbl.setFont(f)
        name_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        text_box.addWidget(name_lbl)

        created = profile.get("created", "")[:10]
        meta_lbl = QLabel(f"Создан: {created}" if created else "")
        meta_lbl.setFont(qt_theme.font("muted"))
        meta_lbl.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        text_box.addWidget(meta_lbl)

        lay.addLayout(text_box, 1)

        # Активная метка
        if is_active:
            badge = QLabel("✓ Активный")
            badge.setFont(qt_theme.font("muted"))
            badge.setStyleSheet(
                f"color: #FFFFFF; background-color: {qt_theme.c('accent')}; "
                f"border-radius: 10px; padding: 4px 12px; font-weight: bold;")
            lay.addWidget(badge)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.profile["id"])
        super().mousePressEvent(event)


class ProfileSwitcherDialog(QDialog):
    """Модальный диалог выбора/управления профилями."""
    profile_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Профили")
        self.resize(520, 600)
        self.setStyleSheet(_dialog_qss())
        self._build()

    def _build(self):
        s = qt_theme.scale
        lay = QVBoxLayout(self)
        lay.setContentsMargins(int(24 * s), int(24 * s),
                               int(24 * s), int(24 * s))
        lay.setSpacing(int(14 * s))

        # Заголовок
        title = QLabel("👥 Профили")
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        lay.addWidget(title)

        hint = QLabel("Выбери профиль или создай новый. "
                      "У каждого профиля свой прогресс.")
        hint.setWordWrap(True)
        hint.setFont(qt_theme.font("body"))
        hint.setStyleSheet(
            f"color: {qt_theme.c('text_muted')}; background: transparent;")
        lay.addWidget(hint)

        # Скролл со списком
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background-color: transparent; border: none; }}
            QScrollBar:vertical {{
                background: rgba(40, 60, 84, 140);
                width: 8px; border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(120, 160, 200, 170);
                border-radius: 4px; min-height: 30px;
            }}
        """)
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        ilay = QVBoxLayout(inner)
        ilay.setContentsMargins(0, 0, 0, 0)
        ilay.setSpacing(int(8 * s))

        active_id = profiles.active_id
        can_delete = len(profiles.list_profiles()) > 1

        for p in profiles.list_profiles():
            card = ProfileCard(p, is_active=(p["id"] == active_id),
                                can_delete=can_delete, parent=self)
            card.clicked.connect(self._switch)
            ilay.addWidget(card)

        ilay.addStretch()
        scroll.setWidget(inner)
        lay.addWidget(scroll, 1)

        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(int(10 * s))

        create_btn = QPushButton("➕  Создать новый профиль")
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setMinimumHeight(int(48 * s))
        create_btn.setStyleSheet(primary_btn_qss("rgba(92, 214, 142, 160)"))
        create_btn.clicked.connect(self._create_new)
        btn_row.addWidget(create_btn)

        # Управление — редактировать/удалить активный
        active = profiles.get_active()
        if active:
            edit_btn = QPushButton("✏")
            edit_btn.setToolTip("Редактировать активный")
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setFixedSize(int(48 * s), int(48 * s))
            edit_btn.setStyleSheet(primary_btn_qss("rgba(74, 158, 255, 160)"))
            edit_btn.clicked.connect(lambda: self._edit(active["id"]))
            btn_row.addWidget(edit_btn)

            if can_delete:
                del_btn = QPushButton("🗑")
                del_btn.setToolTip("Удалить активный")
                del_btn.setCursor(Qt.PointingHandCursor)
                del_btn.setFixedSize(int(48 * s), int(48 * s))
                del_btn.setStyleSheet(primary_btn_qss("rgba(255, 120, 120, 160)"))
                del_btn.clicked.connect(lambda: self._delete(active["id"]))
                btn_row.addWidget(del_btn)

        btn_row.addStretch()
        lay.addLayout(btn_row)

        # Закрыть
        close_btn = QPushButton("Закрыть")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setMinimumHeight(int(40 * s))
        close_btn.setStyleSheet(primary_btn_qss("rgba(80, 100, 130, 160)"))
        close_btn.clicked.connect(self.reject)
        lay.addWidget(close_btn)

    def _switch(self, profile_id):
        if profile_id == profiles.active_id:
            return
        profiles.set_active(profile_id)
        # Перезагружаем storage
        from core.storage import storage
        storage.reload()
        # Применяем язык профиля
        from core.i18n import i18n
        lang = storage.get("language", "ru")
        i18n.set_language(lang)
        self.profile_changed.emit()
        self.accept()

    def _create_new(self):
        dlg = ProfileEditDialog(parent=self)
        if dlg.exec_() == QDialog.Accepted:
            self.profile_changed.emit()
            self.accept()

    def _edit(self, profile_id):
        dlg = ProfileEditDialog(profile_id=profile_id, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            self.profile_changed.emit()
            self.accept()

    def _delete(self, profile_id):
        p = profiles.get(profile_id)
        if not p:
            return
        r = QMessageBox.question(
            self, "⚠",
            f"Удалить профиль «{p['name']}»?\n"
            "Весь прогресс этого профиля будет потерян.",
            QMessageBox.Yes | QMessageBox.No
        )
        if r != QMessageBox.Yes:
            return
        if profiles.delete(profile_id):
            from core.storage import storage
            storage.reload()
            self.profile_changed.emit()
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка",
                                 "Нельзя удалить последний профиль.")


class ProfileEditDialog(QDialog):
    """Создание нового профиля или редактирование существующего."""
    def __init__(self, profile_id=None, parent=None):
        super().__init__(parent)
        self.profile_id = profile_id
        self.is_edit = profile_id is not None
        self.selected_avatar = "👤"
        self.selected_color = "blue"

        # Загружаем существующие данные
        if self.is_edit:
            p = profiles.get(profile_id)
            if p:
                self.selected_avatar = p["avatar"]
                self.selected_color = p["color"]

        self.setWindowTitle("Редактировать профиль" if self.is_edit
                            else "Создать профиль")
        self.resize(520, 620)
        self.setStyleSheet(_dialog_qss())
        self._build()

    def _build(self):
        s = qt_theme.scale
        lay = QVBoxLayout(self)
        lay.setContentsMargins(int(28 * s), int(24 * s),
                               int(28 * s), int(24 * s))
        lay.setSpacing(int(14 * s))

        title = QLabel("✏ Редактировать" if self.is_edit else "➕ Новый профиль")
        title.setFont(qt_theme.font("h2"))
        title.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        lay.addWidget(title)

        # Аватар + превью
        preview_row = QHBoxLayout()
        preview_row.setSpacing(int(16 * s))

        self.preview_avatar = QFrame()
        self.preview_avatar.setFixedSize(int(80 * s), int(80 * s))
        self._update_preview_style()
        prev_lay = QVBoxLayout(self.preview_avatar)
        prev_lay.setContentsMargins(0, 0, 0, 0)
        self.preview_lbl = QLabel(self.selected_avatar)
        self.preview_lbl.setFont(QFont("Segoe UI Emoji", int(40 * s)))
        self.preview_lbl.setAlignment(Qt.AlignCenter)
        self.preview_lbl.setStyleSheet("background: transparent;")
        prev_lay.addWidget(self.preview_lbl)
        preview_row.addWidget(self.preview_avatar)

        preview_row.addStretch()
        lay.addLayout(preview_row)

        # Имя
        name_lbl = QLabel("Имя профиля:")
        name_lbl.setFont(qt_theme.font("body_bold"))
        name_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        lay.addWidget(name_lbl)

        self.name_edit = QLineEdit()
        if self.is_edit:
            p = profiles.get(self.profile_id)
            self.name_edit.setText(p["name"] if p else "")
        self.name_edit.setPlaceholderText("Введите имя...")
        self.name_edit.setMinimumHeight(int(44 * s))
        lay.addWidget(self.name_edit)

        # Аватары
        av_lbl = QLabel("Аватар:")
        av_lbl.setFont(qt_theme.font("body_bold"))
        av_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        lay.addWidget(av_lbl)

        av_grid = QGridLayout()
        av_grid.setSpacing(int(6 * s))
        self.av_buttons = []
        for i, emoji in enumerate(AVATARS):
            b = QPushButton(emoji)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedSize(int(46 * s), int(46 * s))
            b.setFont(QFont("Segoe UI Emoji", int(20 * s)))
            self._style_avatar_button(b, emoji)
            b.clicked.connect(lambda _c=False, e=emoji: self._pick_avatar(e))
            av_grid.addWidget(b, i // 8, i % 8)
            self.av_buttons.append((b, emoji))
        lay.addLayout(av_grid)

        # Цвета
        col_lbl = QLabel("Цвет фона:")
        col_lbl.setFont(qt_theme.font("body_bold"))
        col_lbl.setStyleSheet(
            f"color: {qt_theme.c('text')}; background: transparent;")
        lay.addWidget(col_lbl)

        col_row = QHBoxLayout()
        col_row.setSpacing(int(8 * s))
        self.col_buttons = []
        for name in AVATAR_COLORS:
            color, dark = COLOR_HEX[name]
            b = QPushButton()
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedSize(int(46 * s), int(46 * s))
            border = "3px solid #FFFFFF" if name == self.selected_color else "1px solid rgba(255,255,255,80)"
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: {border};
                    border-radius: {int(12 * s)}px;
                }}
                QPushButton:hover {{
                    border: 3px solid rgba(255,255,255,200);
                }}
            """)
            b.clicked.connect(lambda _c=False, n=name: self._pick_color(n))
            col_row.addWidget(b)
            self.col_buttons.append((b, name))
        col_row.addStretch()
        lay.addLayout(col_row)

        lay.addStretch()

        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(int(10 * s))

        cancel = QPushButton("Отмена")
        cancel.setCursor(Qt.PointingHandCursor)
        cancel.setMinimumHeight(int(44 * s))
        cancel.setStyleSheet(primary_btn_qss("rgba(80, 100, 130, 160)"))
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)

        save = QPushButton("💾 Сохранить")
        save.setCursor(Qt.PointingHandCursor)
        save.setMinimumHeight(int(44 * s))
        save.setStyleSheet(primary_btn_qss("rgba(92, 214, 142, 180)"))
        save.clicked.connect(self._save)
        btn_row.addWidget(save)

        lay.addLayout(btn_row)

    def _update_preview_style(self):
        s = qt_theme.scale
        color, border = COLOR_HEX.get(self.selected_color, COLOR_HEX["blue"])
        self.preview_avatar.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 2px solid {border};
                border-radius: {int(20 * s)}px;
            }}
        """)

    def _style_avatar_button(self, b, emoji):
        s = qt_theme.scale
        if emoji == self.selected_avatar:
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(74, 158, 255, 150);
                    border: 2px solid {qt_theme.c('accent')};
                    border-radius: {int(12 * s)}px;
                }}
            """)
        else:
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(30, 46, 62, 200);
                    border: 1px solid rgba(120, 160, 200, 60);
                    border-radius: {int(12 * s)}px;
                }}
                QPushButton:hover {{
                    background-color: rgba(60, 88, 120, 220);
                }}
            """)

    def _pick_avatar(self, emoji):
        self.selected_avatar = emoji
        self.preview_lbl.setText(emoji)
        for b, e in self.av_buttons:
            self._style_avatar_button(b, e)

    def _pick_color(self, name):
        self.selected_color = name
        self._update_preview_style()
        s = qt_theme.scale
        for b, n in self.col_buttons:
            color, dark = COLOR_HEX[n]
            border = "3px solid #FFFFFF" if n == name else "1px solid rgba(255,255,255,80)"
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: {border};
                    border-radius: {int(12 * s)}px;
                }}
                QPushButton:hover {{
                    border: 3px solid rgba(255,255,255,200);
                }}
            """)

    def _save(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "!", "Введите имя профиля")
            return

        if self.is_edit:
            profiles.update(self.profile_id,
                            name=name,
                            avatar=self.selected_avatar,
                            color=self.selected_color)
        else:
            new_id = profiles.create(name, self.selected_avatar,
                                      self.selected_color)
            # Автоматически делаем активным
            profiles.set_active(new_id)
            from core.storage import storage
            storage.reload()

        self.accept()
