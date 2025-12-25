# -*- coding: utf-8 -*-
"""
Markdown Editor - File operations and unsaved changes control
Operaciones de archivo y control de cambios sin guardar

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
from tkinter import filedialog, messagebox
from .i18n import t
from .config import add_recent_file


class FileManager:
    """
    Manages file operations and dirty flag
    Gestiona operaciones de archivo y flag de cambios
    """
    
    FILETYPES = [
        ("Markdown files", "*.md"),
        ("Text files", "*.txt"),
        ("All files", "*.*")
    ]
    VALID_EXTENSIONS = ('.md', '.txt', '.markdown')
    DEFAULT_NAME = "noname.md"
    
    def __init__(self, editor_widget, on_file_change=None, on_status=None):
        """
        Initialize file manager
        
        Args:
            editor_widget: Text widget to manage
            on_file_change: Callback(filepath, content) on file change
            on_status: Callback(message) for status updates
        """
        self.editor = editor_widget
        self.on_file_change = on_file_change
        self.on_status = on_status
        self.current_file = None
        self.last_saved = ""
        self.last_directory = None
    
    # =========================================================================
    # DIRTY FLAG
    # =========================================================================
    
    def is_dirty(self):
        """Are there unsaved changes?"""
        return self.editor.get("1.0", "end-1c") != self.last_saved
    
    def mark_saved(self, content=None):
        """Mark current content as saved"""
        self.last_saved = content if content else self.editor.get("1.0", "end-1c")
    
    def check_unsaved(self):
        """Ask before losing changes. Returns True to continue."""
        if not self.is_dirty():
            return True
        
        result = messagebox.askyesnocancel(
            t("dialog.unsaved_title"),
            t("dialog.unsaved_msg")
        )
        
        if result is None:  # Cancel
            return False
        if result:  # Yes - save first
            self.save()
            return not self.is_dirty()
        return True  # No - discard changes
    
    # =========================================================================
    # OPERATIONS
    # =========================================================================
    
    def new(self, default_content=""):
        """New file - sets name to noname.md"""
        if not self.check_unsaved():
            return False
        
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", default_content)
        self.current_file = None
        self.last_saved = default_content
        
        if self.on_file_change:
            self.on_file_change(None, default_content)
        if self.on_status:
            self.on_status(f"{t('status.new_document')}: {self.DEFAULT_NAME}")
        return True
    
    def open(self):
        """Open file with dialog, suggesting last directory"""
        if not self.check_unsaved():
            return False
        
        initial_dir = self.last_directory
        if not initial_dir and self.current_file:
            initial_dir = os.path.dirname(self.current_file)
        
        path = filedialog.askopenfilename(
            filetypes=self.FILETYPES,
            initialdir=initial_dir
        )
        if path:
            return self.load(path)
        return False
    
    def load(self, filepath):
        """Load a specific file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            self.current_file = filepath
            self.last_saved = content
            self.last_directory = os.path.dirname(filepath)
            
            if self.on_file_change:
                self.on_file_change(filepath, content)
            if self.on_status:
                self.on_status(f"{t('status.opened')}: {os.path.basename(filepath)}")
            
            # Add to recent files / Añadir a recientes
            add_recent_file(filepath)
            return True
        except Exception as e:
            messagebox.showerror(t("dialog.error"), f"{t('dialog.error_open')}:\n{e}")
            return False
    
    def save(self):
        """Save (or save as if no file)"""
        if self.current_file:
            return self._do_save(self.current_file)
        return self.save_as()
    
    def save_as(self):
        """Save as, suggesting current filename or noname.md"""
        initial_dir = self.last_directory
        if not initial_dir and self.current_file:
            initial_dir = os.path.dirname(self.current_file)
        
        initial_file = self.DEFAULT_NAME
        if self.current_file:
            initial_file = os.path.basename(self.current_file)
        
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=self.FILETYPES[:2],
            initialdir=initial_dir,
            initialfile=initial_file
        )
        if path:
            return self._do_save(path)
        return False
    
    def _do_save(self, filepath):
        """Execute save operation"""
        try:
            content = self.editor.get("1.0", "end-1c")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.current_file = filepath
            self.last_saved = content
            self.last_directory = os.path.dirname(filepath)
            
            if self.on_file_change:
                self.on_file_change(filepath, content)
            if self.on_status:
                self.on_status(f"{t('status.saved')}: {os.path.basename(filepath)}")
            
            # Add to recent files / Añadir a recientes
            add_recent_file(filepath)
            return True
        except Exception as e:
            messagebox.showerror(t("dialog.error"), f"{t('dialog.error_save')}:\n{e}")
            return False
    
    # =========================================================================
    # UTILITIES
    # =========================================================================
    
    def get_filename(self):
        """Current filename or default name"""
        if self.current_file:
            return os.path.basename(self.current_file)
        return self.DEFAULT_NAME
    
    def get_filepath(self):
        """Current full filepath or None"""
        return self.current_file
    
    def get_directory(self):
        """Current file directory or last used directory"""
        if self.current_file:
            return os.path.dirname(self.current_file)
        return self.last_directory
    
    def get_base_name(self):
        """Filename without extension for export suggestions"""
        name = self.get_filename()
        return os.path.splitext(name)[0]
    
    def is_valid_extension(self, filepath):
        """Check if extension is valid"""
        return filepath.lower().endswith(self.VALID_EXTENSIONS)
