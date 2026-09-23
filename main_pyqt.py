
# -*- coding: utf-8 -*-
"""HSK 5 Learner - PyQt5 glass version."""
import sys
import os
import ctypes

# Отключаем шумные предупреждения Qt (DirectWrite, fonts и т.д.)
os.environ["QT_LOGGING_RULES"] = (
    "qt.qpa.fonts.warning=false;"
    "qt.qpa.fonts.debug=false;"
    "qt.text.font.db.warning=false;"
    "qt.text.font.db.debug=false;"
    "*.warning=false;"
    "*.debug=false"
)

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

from qt.theme import qt_theme
from qt.main_window import MainWindow
from core.i18n import i18n
# Автопатч: добавляет UZ/TG к локализации
import core.i18n_uz_tg  # noqa
from core.storage import storage


def detect_dpi_scale(app):
    try:
        return max(1.0, app.primaryScreen().logicalDotsPerInch() / 96.0)
    except Exception:
        return 1.0


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HSK 5 Learner")

    i18n.set_language(storage.get("language", "ru"))
    qt_theme.set_mode(storage.get("theme_mode", "glass"))

    fams = set(QFontDatabase().families())
    cjk = next((f for f in ("Microsoft YaHei UI", "Microsoft YaHei",
                             "SimHei", "SimSun", "Noto Sans CJK SC",
                             "PingFang SC", "Arial Unicode MS") if f in fams),
               "Arial")
    ui = next((f for f in ("Segoe UI", "Helvetica Neue", "Arial")
               if f in fams), "Arial")

    qt_theme.init(cjk_family=cjk, ui_family=ui,
                  dpi_scale=detect_dpi_scale(app))

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
