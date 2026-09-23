# -*- coding: utf-8 -*-
"""Менеджер профилей: несколько пользователей, свои прогрессы."""
import json
import uuid
from datetime import datetime
from pathlib import Path

from core.config import USER_DATA_DIR


PROFILES_FILE = USER_DATA_DIR / "profiles.json"

# Набор доступных эмодзи-аватаров
AVATARS = ["👤", "👨", "👩", "🧑", "👦", "👧", "🐱", "🐶",
           "🦊", "🐼", "🐨", "🦁", "🐸", "🐧", "🦉", "🐙"]

# Набор фоновых цветов для аватара
AVATAR_COLORS = ["blue", "green", "orange", "purple", "pink", "teal"]

COLOR_HEX = {
    "blue":   ("#3A6088", "#5A80A8"),
    "green":  ("#3A7060", "#5A9080"),
    "orange": ("#7A6030", "#9A8050"),
    "purple": ("#5A4A88", "#7A6AA8"),
    "pink":   ("#7A3A60", "#9A5A80"),
    "teal":   ("#3A7080", "#5A90A0"),
}


class ProfileManager:
    """Управляет профилями. Хранит реестр в profiles.json."""

    def __init__(self):
        self._file = PROFILES_FILE
        self._data = self._load()
        self._ensure_default()

    def _load(self) -> dict:
        if not self._file.exists():
            return {"profiles": [], "active_id": None}
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"profiles": [], "active_id": None}

    def _save(self):
        try:
            with open(self._file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[profiles] save error: {e}")

    def _ensure_default(self):
        """Создаёт дефолтный профиль при первом запуске."""
        if not self._data.get("profiles"):
            # Миграция: старый progress.json → профиль "По умолчанию"
            old_progress = USER_DATA_DIR / "progress.json"
            default_id = str(uuid.uuid4())[:8]

            # Имя из старого прогресса
            name = "По умолчанию"
            avatar = "👤"
            color = "blue"
            if old_progress.exists():
                try:
                    with open(old_progress, "r", encoding="utf-8") as f:
                        old_data = json.load(f)
                    if old_data.get("profile_name"):
                        name = old_data["profile_name"]
                    # Перемещаем старый прогресс в новый файл
                    new_path = USER_DATA_DIR / f"profile_{default_id}.json"
                    with open(new_path, "w", encoding="utf-8") as f:
                        json.dump(old_data, f, ensure_ascii=False, indent=2)
                    print(f"[profiles] миграция: progress.json → profile_{default_id}.json")
                except Exception as e:
                    print(f"[profiles] migration error: {e}")

            profile = {
                "id": default_id,
                "name": name,
                "avatar": avatar,
                "color": color,
                "created": datetime.now().isoformat(),
            }
            self._data["profiles"] = [profile]
            self._data["active_id"] = default_id
            self._save()

    # -------------------- API --------------------
    @property
    def active_id(self) -> str:
        return self._data.get("active_id")

    def list_profiles(self) -> list:
        return list(self._data.get("profiles", []))

    def get_active(self) -> dict:
        for p in self.list_profiles():
            if p["id"] == self.active_id:
                return p
        # Fallback: первый
        profiles = self.list_profiles()
        return profiles[0] if profiles else None

    def get(self, profile_id: str) -> dict:
        for p in self.list_profiles():
            if p["id"] == profile_id:
                return p
        return None

    def create(self, name: str, avatar: str = "👤", color: str = "blue") -> str:
        new_id = str(uuid.uuid4())[:8]
        profile = {
            "id": new_id,
            "name": name.strip() or "Новый профиль",
            "avatar": avatar if avatar in AVATARS else "👤",
            "color": color if color in AVATAR_COLORS else "blue",
            "created": datetime.now().isoformat(),
        }
        self._data.setdefault("profiles", []).append(profile)
        self._save()
        return new_id

    def set_active(self, profile_id: str) -> bool:
        if not self.get(profile_id):
            return False
        self._data["active_id"] = profile_id
        self._save()
        return True

    def update(self, profile_id: str, name=None, avatar=None, color=None) -> bool:
        p = self.get(profile_id)
        if not p:
            return False
        if name is not None:
            p["name"] = name.strip() or p["name"]
        if avatar is not None and avatar in AVATARS:
            p["avatar"] = avatar
        if color is not None and color in AVATAR_COLORS:
            p["color"] = color
        self._save()
        return True

    def delete(self, profile_id: str) -> bool:
        """Удаляет профиль. Нельзя удалить последний."""
        profiles = self.list_profiles()
        if len(profiles) <= 1:
            return False
        self._data["profiles"] = [p for p in profiles if p["id"] != profile_id]
        # Удаляем файл прогресса
        try:
            pfile = USER_DATA_DIR / f"profile_{profile_id}.json"
            if pfile.exists():
                pfile.unlink()
        except Exception:
            pass
        # Если удалили активный — переключаемся на первый
        if self._data.get("active_id") == profile_id:
            self._data["active_id"] = self._data["profiles"][0]["id"]
        self._save()
        return True

    def get_active_progress_file(self) -> Path:
        """Путь к файлу прогресса активного профиля."""
        pid = self.active_id
        if not pid:
            return USER_DATA_DIR / "progress.json"
        return USER_DATA_DIR / f"profile_{pid}.json"


# Синглтон
profiles = ProfileManager()
