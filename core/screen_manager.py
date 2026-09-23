# -*- coding: utf-8 -*-
"""
Менеджер экранов.
Позволяет регистрировать экраны и переключаться между ними с передачей аргументов.
"""
from typing import Callable, Dict, Any, Optional


class ScreenManager:
    def __init__(self, container):
        self.container = container
        self._registry: Dict[str, Callable] = {}
        self._current_name: Optional[str] = None
        self._current_view = None
        self._history: list = []

    def register(self, name: str, factory: Callable):
        """factory(parent, manager, **kwargs) -> виджет-экран."""
        self._registry[name] = factory

    def show(self, name: str, push_history: bool = True, **kwargs):
        if name not in self._registry:
            raise KeyError(f"Экран '{name}' не зарегистрирован")

        # Запоминаем текущий экран в истории
        if push_history and self._current_name:
            self._history.append((self._current_name, {}))

        # Уничтожаем старый
        if self._current_view is not None:
            try:
                self._current_view.destroy()
            except Exception:
                pass

        factory = self._registry[name]
        self._current_view = factory(self.container, self, **kwargs)
        self._current_view.pack(fill="both", expand=True)
        self._current_name = name

    def back(self):
        """Возвращает на предыдущий экран."""
        if not self._history:
            return
        prev_name, kwargs = self._history.pop()
        self.show(prev_name, push_history=False, **kwargs)

    @property
    def current(self) -> Optional[str]:
        return self._current_name