# -*- coding: utf-8 -*-
"""
Markdown Editor - Zoom functions for editor and preview
Funciones de zoom para editor y preview

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

from .config import get_ui_config, update_ui_config


class ZoomManager:
    """
    Manages zoom for editor and preview
    Gestiona el zoom del editor y preview
    """
    
    # Limits / Límites
    EDITOR_MIN = 10
    EDITOR_MAX = 36
    PREVIEW_MIN = 10
    PREVIEW_MAX = 32
    STEP = 2
    
    def __init__(self, editor_widget, status_callback=None):
        """
        Initialize zoom manager
        Inicializa gestor de zoom
        
        Args:
            editor_widget: Text widget to zoom / Widget de texto a hacer zoom
            status_callback: Callback(message) for status updates / Callback para actualizar estado
        """
        self.editor = editor_widget
        self.status_callback = status_callback
        
        # Load from config / Cargar desde config
        ui_config = get_ui_config()
        self.editor_size = ui_config.get("editor_font_size", 14)
        self.preview_size = ui_config.get("preview_font_size", 16)
        
        # Apply initial editor size / Aplicar tamaño inicial del editor
        self._apply_editor_font(save=False)
    
    # =========================================================================
    # EDITOR ZOOM
    # =========================================================================
    
    def editor_in(self):
        """Zoom in editor / Aumentar zoom editor"""
        if self.editor_size < self.EDITOR_MAX:
            self.editor_size += self.STEP
            self._apply_editor_font()
    
    def editor_out(self):
        """Zoom out editor / Reducir zoom editor"""
        if self.editor_size > self.EDITOR_MIN:
            self.editor_size -= self.STEP
            self._apply_editor_font()
    
    def editor_reset(self):
        """Reset editor zoom / Resetear zoom editor"""
        self.editor_size = get_ui_config().get("editor_font_size", 14)
        self._apply_editor_font()
    
    def _apply_editor_font(self, save=True):
        """Apply font size to editor / Aplica tamaño de fuente al editor"""
        self.editor.configure(font=("Consolas", self.editor_size))
        if save:
            update_ui_config(editor_font_size=self.editor_size)
        if self.status_callback:
            self.status_callback(f"Editor: {self.editor_size}px")
    
    def get_editor_size(self):
        """Get current editor font size / Obtiene tamaño actual del editor"""
        return self.editor_size
    
    # =========================================================================
    # PREVIEW ZOOM
    # =========================================================================
    
    def preview_in(self):
        """Zoom in preview / Aumentar zoom preview"""
        if self.preview_size < self.PREVIEW_MAX:
            self.preview_size += self.STEP
            update_ui_config(preview_font_size=self.preview_size)
            return True
        return False
    
    def preview_out(self):
        """Zoom out preview / Reducir zoom preview"""
        if self.preview_size > self.PREVIEW_MIN:
            self.preview_size -= self.STEP
            update_ui_config(preview_font_size=self.preview_size)
            return True
        return False
    
    def preview_reset(self):
        """Reset preview zoom / Resetear zoom preview"""
        self.preview_size = 16
        update_ui_config(preview_font_size=self.preview_size)
    
    def get_preview_size(self):
        """Get current preview font size / Obtiene tamaño actual del preview"""
        return self.preview_size
    
    def get_preview_zoom_text(self):
        """
        Get preview zoom as text (px)
        Obtiene zoom del preview como texto (px)
        """
        return f"{self.preview_size}px"
    
    def get_zoom_css(self):
        """
        Get CSS for preview zoom by setting font-size.
        Obtiene CSS para zoom del preview estableciendo font-size.
        """
        return f"""html {{
    font-size: {self.preview_size}px !important;
}}
body {{
    font-size: inherit !important;
    padding: 10px 15px !important;
    margin: 0 !important;
}}
h1 {{ font-size: 2em !important; }}
h2 {{ font-size: 1.5em !important; }}
h3 {{ font-size: 1.25em !important; }}
pre, code {{ font-size: 0.9em !important; }}
"""
