# -*- coding: utf-8 -*-
"""
Markdown Editor - Main entry point
Punto de entrada principal

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

# DPI awareness for Windows 10/11 with 4K displays
# Soporte DPI para Windows 10/11 con pantallas 4K
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

from modules.app import MarkdownEditor

if __name__ == "__main__":
    app = MarkdownEditor()
    app.mainloop()
