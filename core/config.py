# -*- coding: utf-8 -*-
"""
Конфигурация приложения HSK 5 Learner.
Здесь хранятся все глобальные настройки — пути, версия, дефолтные значения.
"""
from pathlib import Path

# --- Метаданные приложения ---
APP_NAME = "HSK 5 Learner"
APP_VERSION = "0.1.0"
APP_AUTHOR = "HSK5 Project"

# --- Пути ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LESSONS_DIR = DATA_DIR / "lessons"
USER_DATA_DIR = Path.home() / ".hsk5_learner"
PROGRESS_FILE = USER_DATA_DIR / "progress.json"

# Создаём папку пользователя при первом запуске
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Языки интерфейса ---
SUPPORTED_LANGUAGES = ["ru", "tk", "en", "uz", "tg"]
DEFAULT_LANGUAGE = "ru"

# --- Окно ---
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600

# --- Структура учебника ---
TOTAL_UNITS = 6
LESSONS_PER_UNIT = 3
TOTAL_LESSONS = TOTAL_UNITS * LESSONS_PER_UNIT

# Названия юнитов (на трёх языках)
UNIT_TITLES = {
    1: {"zh": "了解生活", "ru": "Понимание жизни", "tk": "Durmuşy düşünmek", "en": "Understanding Life"},
    2: {"zh": "谈古说今", "ru": "О прошлом и настоящем", "tk": "Geçmiş we häzirki zaman", "en": "Past and Present"},
    3: {"zh": "倾听故事", "ru": "Слушаем истории", "tk": "Hekaýalary diňlemek", "en": "Listening to Stories"},
    4: {"zh": "走近科学", "ru": "Ближе к науке", "tk": "Ylyma ýakynlaşmak", "en": "Approaching Science"},
    5: {"zh": "放眼世界", "ru": "Взгляд на мир", "tk": "Dünýä nazary", "en": "Seeing the World"},
    6: {"zh": "修养身心", "ru": "Совершенствование души и тела", "tk": "Ruhy we beden taýdan kämilleşmek", "en": "Cultivating Body and Mind"},
}