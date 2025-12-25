# -*- coding: utf-8 -*-
"""
Markdown Editor - Toolbar creation
Creación de barra de herramientas

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import customtkinter as ctk

from .config import UI_FONT_FAMILY, UI_FONT_SIZE
from .icons import get_icon_text
from .styles import get_style_names
from .i18n import t
from . import i18n


def create_toolbar(app):
    """
    Create and configure toolbar for the application
    Crea y configura la barra de herramientas para la aplicación
    
    Args:
        app: MarkdownEditor instance
    
    Returns:
        CTkFrame: The toolbar frame
    """
    toolbar = ctk.CTkFrame(app, height=45)
    toolbar.pack(fill="x", padx=5, pady=5)
    
    ui_font = (UI_FONT_FAMILY, UI_FONT_SIZE)
    btn_cfg = {
        "height": 36, "width": 44, 
        "font": ("Segoe UI Emoji", 18),
        "fg_color": "transparent", 
        "hover_color": ("gray75", "gray25"),
        "text_color": ("gray10", "gray90")
    }
    
    # File buttons
    _create_icon_btn(app, toolbar, "new", app._new, "tooltip.new", btn_cfg)
    _create_icon_btn(app, toolbar, "open", app._open, "tooltip.open", btn_cfg)
    _create_icon_btn(app, toolbar, "save", app._save, "tooltip.save", btn_cfg)
    
    # Save As - text button
    app.btn_saveas = ctk.CTkButton(
        toolbar, text=t("label.save_as_btn"), width=50, height=36, 
        font=ui_font, fg_color="transparent",
        hover_color=("gray75", "gray25"),
        text_color=("gray10", "gray90"),
        command=app._save_as
    )
    app.btn_saveas.pack(side="left", padx=1)
    app.tooltip_mgr.add_tooltip(app.btn_saveas, "tooltip.save_as")
    
    # Separator
    ctk.CTkFrame(toolbar, width=2, height=28, fg_color="gray50").pack(side="left", padx=8)
    
    # Edit buttons
    _create_icon_btn(app, toolbar, "cut", app._cut, "tooltip.cut", btn_cfg)
    _create_icon_btn(app, toolbar, "copy", app._copy, "tooltip.copy", btn_cfg)
    _create_icon_btn(app, toolbar, "paste", app._paste, "tooltip.paste", btn_cfg)
    
    # Separator
    ctk.CTkFrame(toolbar, width=2, height=28, fg_color="gray50").pack(side="left", padx=8)
    
    # Undo/Redo
    _create_icon_btn(app, toolbar, "undo", app._undo, "tooltip.undo", btn_cfg)
    _create_icon_btn(app, toolbar, "redo", app._redo, "tooltip.redo", btn_cfg)
    
    # Right side frame
    sf = ctk.CTkFrame(toolbar, fg_color="transparent")
    sf.pack(side="right", padx=5)
    
    # Export buttons
    btn_exp = {"font": ui_font, "height": 32}
    pdf_btn = ctk.CTkButton(sf, text="PDF", width=50, command=app._export_pdf, **btn_exp)
    pdf_btn.pack(side="right", padx=2)
    app.tooltip_mgr.add_tooltip(pdf_btn, "tooltip.export_pdf")
    
    html_btn = ctk.CTkButton(sf, text="HTML", width=50, command=app._copy_html, **btn_exp)
    html_btn.pack(side="right", padx=2)
    app.tooltip_mgr.add_tooltip(html_btn, "tooltip.copy_html")
    
    # Separator
    ctk.CTkFrame(sf, width=2, height=28, fg_color="gray50").pack(side="right", padx=8)
    
    # Style selector
    app.style_label = ctk.CTkLabel(sf, text=t("label.style"), font=ui_font)
    app.style_label.pack(side="left", padx=5)
    
    app.style_combo = ctk.CTkComboBox(
        sf, width=180, font=ui_font, height=32,
        values=get_style_names(app.available_styles),
        command=app._on_style_change,
        dropdown_font=ui_font
    )
    app.style_combo.pack(side="left")
    app.style_combo.set(app.current_style.get('name', 'Default'))
    
    ctk.CTkButton(sf, text="...", width=32, command=app._edit_style, **btn_exp).pack(side="left", padx=2)
    
    # Language button
    app.lang_btn = ctk.CTkButton(
        sf, text=i18n.get_current_flag(), width=44, height=36,
        font=("Segoe UI Emoji", 18), fg_color="transparent",
        hover_color=("gray75", "gray25"),
        text_color=("gray10", "gray90"),
        command=app._show_language_menu
    )
    app.lang_btn.pack(side="left", padx=(10, 2))
    app.tooltip_mgr.add_tooltip(app.lang_btn, "tooltip.change_language")
    
    # Theme button
    app.theme_btn = ctk.CTkButton(
        sf, text=get_icon_text("theme_light"), width=44, height=36,
        font=("Segoe UI Emoji", 18), fg_color="transparent",
        hover_color=("gray75", "gray25"), 
        text_color=("gray10", "gray90"),
        command=app._toggle_theme_btn
    )
    app.theme_btn.pack(side="left", padx=(10, 2))
    app.tooltip_mgr.add_tooltip(app.theme_btn, "tooltip.change_theme")
    
    return toolbar


def _create_icon_btn(app, parent, icon_name, command, tooltip, btn_cfg, side="left"):
    """Create toolbar button with emoji icon and tooltip"""
    btn = ctk.CTkButton(parent, text=get_icon_text(icon_name), command=command, **btn_cfg)
    btn.pack(side=side, padx=1)
    app.tooltip_mgr.add_tooltip(btn, tooltip)
    return btn


def update_toolbar_texts(app):
    """
    Update toolbar button texts/tooltips on language change
    Actualiza textos/tooltips de la toolbar al cambiar idioma
    """
    if hasattr(app, 'btn_saveas'):
        app.btn_saveas.configure(text=t("label.save_as_btn"))
    if hasattr(app, 'style_label'):
        app.style_label.configure(text=t("label.style"))
