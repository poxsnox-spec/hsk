# -*- coding: utf-8 -*-
"""
Менеджер аудио. Работает через системный проигрыватель (без сторонних библиотек).
Если файла нет — молча ничего не делает, кнопки в UI становятся неактивны.
"""
import os
import platform
import subprocess
import threading
from pathlib import Path
from core.config import DATA_DIR

AUDIO_DIR = DATA_DIR / "audio"


class AudioManager:
    def __init__(self):
        self._system = platform.system()
        self._current_proc = None

    def find(self, unit: int, lesson: int, filename: str):
        path = AUDIO_DIR / f"unit{unit}" / f"lesson{lesson:02d}" / filename
        return path if path.exists() else None

    def exists(self, unit: int, lesson: int, filename: str) -> bool:
        return self.find(unit, lesson, filename) is not None

    def play(self, path):
        if path is None or not Path(path).exists():
            return
        threading.Thread(target=self._play_sync, args=(Path(path),), daemon=True).start()

    def _play_sync(self, path: Path):
        try:
            if self._system == "Windows":
                os.startfile(str(path))
            elif self._system == "Darwin":
                subprocess.run(["afplay", str(path)], check=False)
            else:
                for player in ("mpv", "aplay", "ffplay", "xdg-open"):
                    if self._which(player):
                        subprocess.run([player, str(path)], check=False)
                        return
        except Exception as e:
            print(f"[audio] ошибка воспроизведения: {e}")

    @staticmethod
    def _which(name):
        return any(
            os.access(os.path.join(p, name), os.X_OK)
            for p in os.environ.get("PATH", "").split(os.pathsep)
        )


audio = AudioManager()