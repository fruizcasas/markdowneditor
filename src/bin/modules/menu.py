# -*- coding: utf-8 -*-
"""
Markdown Editor - Menu bar creation
Creación de barra de menú

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
import customtkinter as ctk
from tkinter import Menu

from .config import APP_NAME, APP_VERSION
from .i18n import t
from . import i18n


def create_menu_bar(app):
    """
    Create and configure menu bar for the application
    Crea y configura la barra de menú para la aplicación
    
    Args:
        app: MarkdownEditor instance
    
    Returns:
        Menu: The configured menu bar
    """
    menu_bar = Menu(app)
    app.configure(menu=menu_bar)
    
    # File menu
    fm = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=t("menu.file"), menu=fm)
    fm.add_command(label=t("menu.new"), command=app._new, accelerator="Ctrl+N")
    fm.add_command(label=t("menu.open"), command=app._open, accelerator="Ctrl+O")
    
    app.recent_menu = Menu(fm, tearoff=0)
    fm.add_cascade(label=t("menu.recent_files"), menu=app.recent_menu)
    
    fm.add_command(label=t("menu.save"), command=app._save, accelerator="Ctrl+S")
    fm.add_command(label=t("menu.save_as"), command=app._save_as, accelerator="Ctrl+Shift+S")
    fm.add_separator()
    fm.add_command(label=t("menu.export_pdf"), command=app._export_pdf)
    fm.add_command(label=t("menu.copy_html"), command=app._copy_html)
    fm.add_separator()
    fm.add_command(label=t("menu.exit"), command=app._on_close)
    
    # Edit menu
    em = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=t("menu.edit"), menu=em)
    em.add_command(label=t("menu.undo"), command=app._undo, accelerator="Ctrl+Z")
    em.add_command(label=t("menu.redo"), command=app._redo, accelerator="Ctrl+Y")
    em.add_separator()
    em.add_command(label=t("menu.cut"), command=app._cut, accelerator="Ctrl+X")
    em.add_command(label=t("menu.copy"), command=app._copy, accelerator="Ctrl+C")
    em.add_command(label=t("menu.paste"), command=app._paste, accelerator="Ctrl+V")
    em.add_separator()
    em.add_command(label=t("menu.find"), command=app._show_find, accelerator="Ctrl+F")
    em.add_command(label=t("menu.replace"), command=app._show_replace, accelerator="Ctrl+H")
    
    # View menu
    vm = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=t("menu.view"), menu=vm)
    vm.add_command(label=t("menu.zoom_in"), command=lambda: (app.zoom.editor_in(), app._update_editor_zoom_label()), accelerator="Ctrl++")
    vm.add_command(label=t("menu.zoom_out"), command=lambda: (app.zoom.editor_out(), app._update_editor_zoom_label()), accelerator="Ctrl+-")
    vm.add_command(label=t("menu.zoom_reset"), command=lambda: (app.zoom.editor_reset(), app._update_editor_zoom_label()), accelerator="Ctrl+0")
    vm.add_separator()
    vm.add_checkbutton(label=t("menu.dark_mode"), variable=app.is_dark_mode, command=app._toggle_theme)
    vm.add_separator()
    
    # Language submenu
    lang_menu = Menu(vm, tearoff=0)
    current_flag = i18n.get_current_flag()
    vm.add_cascade(label=f"{current_flag}  {t('menu.language')}", menu=lang_menu)
    current_lang = i18n.get_current_language()
    for code, flag, display in i18n.get_language_flag_list():
        lang_menu.add_radiobutton(
            label=f"{flag}  {display}",
            command=lambda c=code: i18n.set_language(c),
            value=code,
            variable=ctk.StringVar(value=current_lang)
        )
    
    # Styles menu
    app.styles_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=t("menu.styles"), menu=app.styles_menu)
    
    # Help menu
    hm = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=t("menu.help"), menu=hm)
    hm.add_command(label=t("menu.about"), command=app._show_about)
    
    app.protocol("WM_DELETE_WINDOW", app._on_close)
    
    return menu_bar


def update_styles_menu(app):
    """
    Rebuild styles menu with current styles
    Reconstruye menú de estilos con estilos actuales
    """
    app.styles_menu.delete(0, "end")
    for fname, style in app.available_styles.items():
        app.styles_menu.add_command(
            label=style.get('name', fname),
            command=lambda s=style: app._apply_style(s)
        )
    app.styles_menu.add_separator()
    app.styles_menu.add_command(label=t("menu.edit_style"), command=app._edit_style)
    app.styles_menu.add_command(label=t("menu.reload_styles"), command=app._reload_styles)


def update_recent_menu(app):
    """
    Rebuild recent files menu
    Reconstruye menú de archivos recientes
    """
    from .config import get_recent_files, remove_recent_file
    from tkinter import messagebox
    
    app.recent_menu.delete(0, "end")
    recent = get_recent_files()
    
    if not recent:
        app.recent_menu.add_command(label=t("menu.no_recent"), state="disabled")
    else:
        for filepath in recent:
            filename = os.path.basename(filepath)
            app.recent_menu.add_command(
                label=filename,
                command=lambda p=filepath: app._open_recent(p)
            )
        app.recent_menu.add_separator()
        app.recent_menu.add_command(label=t("menu.clear_recent"), command=app._manage_recent)
