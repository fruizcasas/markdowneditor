# -*- coding: utf-8 -*-
"""
Markdown Editor - Recent files manager dialog
Diálogo de gestión de archivos recientes

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
import customtkinter as ctk
from tkinter import messagebox

from .config import get_recent_files, remove_recent_file, clear_recent_files, UI_FONT_FAMILY, UI_FONT_SIZE
from .i18n import t


class RecentFilesManager:
    """
    Dialog to manage recent files list
    Diálogo para gestionar lista de archivos recientes
    """
    
    def __init__(self, parent, on_update_callback):
        """
        Initialize manager
        
        Args:
            parent: Parent window
            on_update_callback: Called when recent list changes (to update menu)
        """
        self.parent = parent
        self.on_update = on_update_callback
        self.ui_font = (UI_FONT_FAMILY, UI_FONT_SIZE)
    
    def show(self):
        """Show the recent files manager dialog / Muestra el diálogo"""
        recent = get_recent_files()
        
        if not recent:
            messagebox.showinfo(t("dialog.recent_title"), t("menu.no_recent"))
            return
        
        # Create dialog / Crear diálogo
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(t("dialog.recent_title"))
        self.dialog.geometry("500x350")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center on parent / Centrar sobre padre
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() - 500) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - 350) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Scrollable frame for checkboxes / Frame con scroll para checkboxes
        scroll_frame = ctk.CTkScrollableFrame(self.dialog, height=250)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create checkboxes for each file / Crear checkboxes para cada archivo
        self.checkboxes = []
        for filepath in recent:
            var = ctk.BooleanVar(value=False)
            filename = os.path.basename(filepath)
            folder = os.path.dirname(filepath)
            # Shorten folder if too long / Acortar carpeta si es muy larga
            if len(folder) > 40:
                folder = "..." + folder[-37:]
            display_text = f"{filename}  ({folder})"
            
            cb = ctk.CTkCheckBox(scroll_frame, text=display_text, variable=var,
                                 font=self.ui_font, checkbox_width=20, checkbox_height=20)
            cb.pack(anchor="w", pady=2, padx=5)
            self.checkboxes.append((filepath, var))
        
        # Buttons frame / Frame de botones
        btn_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text=t("dialog.recent_delete_selected"), 
                      command=self._delete_selected, font=self.ui_font).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=t("dialog.recent_clear_all"),
                      command=self._clear_all, font=self.ui_font).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=t("dialog.recent_close"),
                      command=self.dialog.destroy, font=self.ui_font).pack(side="right", padx=5)
    
    def _delete_selected(self):
        """Delete selected files from recent / Eliminar seleccionados de recientes"""
        deleted = False
        for filepath, var in self.checkboxes:
            if var.get():
                remove_recent_file(filepath)
                deleted = True
        
        if deleted:
            self.on_update()
            self.dialog.destroy()
            # Reopen if there are still files / Reabrir si aún hay archivos
            if get_recent_files():
                self.show()
        else:
            messagebox.showinfo(t("dialog.recent_title"), t("dialog.recent_none_selected"))
    
    def _clear_all(self):
        """Clear all recent files / Limpiar todos los recientes"""
        clear_recent_files()
        self.on_update()
        self.dialog.destroy()
