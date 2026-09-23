# -*- coding: utf-8 -*-
"""Карточка с иероглифом + озвучкой."""
import tkinter as tk
from core.theme import theme
from core.audio import audio


class HanziCard(tk.Frame):
    def __init__(self, parent, entry, unit=1, lesson=1, show_audio=True):
        super().__init__(parent, bg=theme.c("card"),
                         highlightbackground=theme.c("border"),
                         highlightthickness=1)
        self.entry = entry

        # --- Hanzi ---
        hanzi_lbl = tk.Label(self, text=entry.hanzi,
                             font=theme.font("hanzi_m"),
                             bg=theme.c("card"), fg=theme.c("text"))
        hanzi_lbl.grid(row=0, column=0, sticky="w", padx=(16, 8), pady=(14, 0))

        # --- кнопка 🔊 ---
        if show_audio:
            audio_file = getattr(entry, "audio", "") or ""
            has_audio = bool(audio_file) and audio.exists(unit, lesson, audio_file)
            tk.Button(
                self, text="🔊", font=(theme.ui_family, 12),
                bg=theme.c("card"),
                fg=theme.c("accent") if has_audio else theme.c("text_muted"),
                relief="flat", cursor="hand2" if has_audio else "",
                state="normal" if has_audio else "disabled",
                command=(lambda a=audio_file, u=unit, l=lesson:
                         audio.play(audio.find(u, l, a))) if has_audio else None,
            ).grid(row=0, column=1, sticky="e", padx=(0, 12), pady=(14, 0))

        # --- Pinyin ---
        tk.Label(self, text=entry.pinyin, font=theme.font("pinyin"),
                 bg=theme.c("card"), fg=theme.c("accent")).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=16)

        # --- POS + значение ---
        pos = f"  {entry.pos}" if entry.pos else ""
        tk.Label(self, text=f"{entry.translate('ru')}{pos}",
                 font=theme.font("body"), bg=theme.c("card"),
                 fg=theme.c("text_muted")).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=16, pady=(2, 14))

        self.grid_columnconfigure(0, weight=1)