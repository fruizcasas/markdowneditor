# -*- coding: utf-8 -*-
"""
Markdown Editor - Tooltip system for widgets
Sistema de tooltips para widgets

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import customtkinter as ctk
from .config import UI_FONT_FAMILY
from .i18n import t


class TooltipManager:
    """
    Singleton tooltip manager - ensures only one tooltip visible at a time
    Gestor de tooltips singleton - asegura que solo uno sea visible a la vez
    """
    
    def __init__(self, root):
        """
        Initialize tooltip manager
        
        Args:
            root: Root window for tooltips
        """
        self.root = root
        self._tooltip_window = None
        self._tooltip_job = None
        self._tooltip_widget = None
    
    def add_tooltip(self, widget, key_or_text, is_key=True):
        """
        Add tooltip to widget
        Añade tooltip al widget
        
        Args:
            widget: Widget to add tooltip to
            key_or_text: i18n key (e.g. 'tooltip.save') or plain text
            is_key: If True, key_or_text is a translation key; if False, it's plain text
        """
        widget._tt_key = key_or_text if is_key else None
        widget._tt_text = None if is_key else key_or_text
        widget.bind("<Enter>", lambda e: self._schedule(widget))
        widget.bind("<Leave>", lambda e: self._hide())
        widget.bind("<Button-1>", lambda e: self._hide())
    
    def _schedule(self, widget):
        """Schedule tooltip show after delay / Programa mostrar tooltip tras delay"""
        self._hide()
        self._tooltip_widget = widget
        self._tooltip_job = self.root.after(400, lambda: self._show(widget))
    
    def _show(self, widget):
        """Show tooltip for widget / Muestra tooltip para widget"""
        if not widget.winfo_exists():
            return
        if self._tooltip_widget != widget:
            return
        
        x = widget.winfo_rootx() + widget.winfo_width() // 2
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        
        self._tooltip_window = ctk.CTkToplevel(self.root)
        self._tooltip_window.wm_overrideredirect(True)
        self._tooltip_window.wm_geometry(f"+{x}+{y}")
        self._tooltip_window.attributes("-topmost", True)
        
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#2b2b2b" if is_dark else "#f0f0f0"
        text_color = "#ffffff" if is_dark else "#000000"
        
        # Get text: translate key or use plain text
        tooltip_text = t(widget._tt_key) if widget._tt_key else widget._tt_text
        
        lbl = ctk.CTkLabel(
            self._tooltip_window, text=tooltip_text,
            font=(UI_FONT_FAMILY, 11), fg_color=bg_color,
            text_color=text_color, corner_radius=4, padx=10, pady=6
        )
        lbl.pack()
        
        # Auto-hide after 2.5 seconds
        self._tooltip_job = self.root.after(2500, self._hide)
    
    def _hide(self):
        """Hide and cleanup tooltip / Oculta y limpia tooltip"""
        if self._tooltip_job:
            try:
                self.root.after_cancel(self._tooltip_job)
            except:
                pass
            self._tooltip_job = None
        
        if self._tooltip_window:
            try:
                self._tooltip_window.destroy()
            except:
                pass
            self._tooltip_window = None
        
        self._tooltip_widget = None
