# -*- coding: utf-8 -*-
"""
Markdown Editor - Drag & Drop support using windnd
Soporte Drag & Drop usando windnd

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

DND_AVAILABLE = False

try:
    import windnd
    DND_AVAILABLE = True
except ImportError:
    windnd = None


def setup_window_drop(window, callback):
    """
    Enable drag & drop on window. callback(filepath) when file dropped.
    Activa DnD en la ventana. callback(filepath) al soltar archivo.
    """
    
    if not DND_AVAILABLE:
        return False
    
    try:
        def on_drop(files):
            if files and len(files) > 0:
                f = files[0]
                filepath = f.decode('utf-8', errors='replace') if isinstance(f, bytes) else str(f)
                callback(filepath)
        
        windnd.hook_dropfiles(window, func=on_drop)
        return True
    except:
        return False
