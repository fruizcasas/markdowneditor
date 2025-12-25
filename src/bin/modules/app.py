# -*- coding: utf-8 -*-
"""
Markdown Editor - Main application window
Ventana principal de la aplicación

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
import customtkinter as ctk
from tkinter import messagebox, Menu, PanedWindow, HORIZONTAL

from .config import (APP_NAME, APP_VERSION, UI_FONT_FAMILY, UI_FONT_SIZE, 
                     UI_FONT_SIZE_HEADER, EDITOR_FONT_SIZE,
                     get_recent_files, add_recent_file, remove_recent_file)
from .snippets import get_snippets, get_example_document
from .styles import load_all_styles, save_style, get_default_style, get_style_names
from .style_editor import StyleEditorWindow
from .renderer import render_full_html
from .exporter import open_html_in_browser, export_to_pdf
from .dnd_support import setup_window_drop
from .zoom import ZoomManager
from .file_ops import FileManager
from .icons import get_icon_text, init_icons
from .find_replace import FindReplaceBar
from .tooltips import TooltipManager
from .recent_manager import RecentFilesManager
from .menu import create_menu_bar, update_styles_menu, update_recent_menu
from .toolbar import create_toolbar, update_toolbar_texts
from . import i18n
from .i18n import t

try:
    from tkinterweb import HtmlFrame
    HTMLFRAME_AVAILABLE = True
except ImportError:
    HTMLFRAME_AVAILABLE = False


class MarkdownEditor(ctk.CTk):
    """
    Main editor class with split view (editor + preview)
    Clase principal del editor con vista dividida (editor + preview)
    """
    
    def __init__(self):
        super().__init__()
        
        i18n.init()
        i18n.on_language_change(self._on_language_change)
        init_icons(self)
        
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1400x900")
        
        self.is_dark_mode = ctk.BooleanVar(value=True)
        self.update_job = None
        self.current_style = None
        self.available_styles = {}
        
        self.ui_font = (UI_FONT_FAMILY, UI_FONT_SIZE)
        self.ui_font_bold = (UI_FONT_FAMILY, UI_FONT_SIZE_HEADER, "bold")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.tooltip_mgr = TooltipManager(self)
        self.recent_mgr = RecentFilesManager(self, self._update_recent_menu)
        
        self._load_styles()
        self._create_ui()
        self._setup_managers()
        self._setup_bindings()
        
        self.dnd_enabled = setup_window_drop(self, self._on_drop)
        
        self._init_document()
        self._update_status_dnd()
    
    def _load_styles(self):
        """Load available CSS styles"""
        self.available_styles = load_all_styles()
        for name in ['gitlab.json', 'default.json']:
            if name in self.available_styles:
                self.current_style = self.available_styles[name]
                break
        if not self.current_style:
            self.current_style = get_default_style()
    
    def _create_ui(self):
        """Create all UI elements"""
        self.menu_bar = create_menu_bar(self)
        self._update_recent_menu()
        update_styles_menu(self)
        self.toolbar = create_toolbar(self)
        self._create_main_area()
        self._create_status_bar()
    
    def _setup_managers(self):
        """Initialize zoom and file managers"""
        from .config import get_ui_config
        
        self.zoom = ZoomManager(self.editor, lambda m: self.status_label.configure(text=m))
        self.file_mgr = FileManager(
            self.editor,
            on_file_change=self._on_file_change,
            on_status=lambda m: self.status_label.configure(text=m)
        )
        
        ui_config = get_ui_config()
        self.zoom_label.configure(text=self.zoom.get_preview_zoom_text())
        self.editor_zoom_label.configure(text=f"{self.zoom.editor_size}px")
        self.preview_frozen.set(ui_config.get("preview_frozen", False))
    
    def _init_document(self):
        """Load example document"""
        example = get_example_document()
        self.editor.insert("1.0", example)
        self.file_mgr.mark_saved(example)
        self.file_label.configure(text=self.file_mgr.get_filename())
        self._update_title()
        self._force_update_preview()
    
    # =========================================================================
    # LANGUAGE CHANGE
    # =========================================================================
    
    def _on_language_change(self):
        """Rebuild UI when language changes"""
        self.menu_bar.destroy()
        self.menu_bar = create_menu_bar(self)
        self._update_recent_menu()
        update_styles_menu(self)
        self._create_context_menu()
        update_toolbar_texts(self)
        self._update_panel_texts()
        self._update_status_dnd()
        
        if hasattr(self, 'lang_btn'):
            self.lang_btn.configure(text=i18n.get_current_flag())
    
    def _update_panel_texts(self):
        """Update panel header labels"""
        if hasattr(self, 'editor_title_label'):
            self.editor_title_label.configure(text=t("panel.editor"))
        if hasattr(self, 'preview_title_label'):
            self.preview_title_label.configure(text=t("panel.preview"))
    
    def _update_recent_menu(self):
        """Rebuild recent files menu"""
        update_recent_menu(self)
    
    # =========================================================================
    # MAIN AREA
    # =========================================================================
    
    def _create_main_area(self):
        """Create split view with editor and preview"""
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.paned = PanedWindow(
            self.main_frame, orient=HORIZONTAL, 
            sashwidth=10, sashrelief="raised", bg="#3b3b3b"
        )
        self.paned.pack(fill="both", expand=True)
        
        self.editor_expanded = True
        self.preview_expanded = True
        
        # Editor panel
        self.editor_frame = ctk.CTkFrame(self.paned)
        self.paned.add(self.editor_frame, minsize=150, stretch="always")
        
        eh = ctk.CTkFrame(self.editor_frame, height=35)
        eh.pack(fill="x")
        
        self.editor_title_label = ctk.CTkLabel(eh, text=t("panel.editor"), font=self.ui_font_bold)
        self.editor_title_label.pack(side="left", padx=10)
        
        self.editor_collapse_btn = ctk.CTkButton(
            eh, text="▶", width=25, height=24,
            command=self._toggle_preview_collapse, font=self.ui_font
        )
        self.editor_collapse_btn.pack(side="right", padx=5)
        
        # Editor zoom
        ezf = ctk.CTkFrame(eh, fg_color="transparent")
        ezf.pack(side="right", padx=5)
        
        ctk.CTkButton(ezf, text="A+", width=30, height=24,
            command=lambda: self.zoom.editor_in() or self._update_editor_zoom_label(),
            font=self.ui_font).pack(side="right", padx=2)
        self.editor_zoom_label = ctk.CTkLabel(ezf, text=f"{EDITOR_FONT_SIZE}px", font=self.ui_font, width=40)
        self.editor_zoom_label.pack(side="right", padx=2)
        ctk.CTkButton(ezf, text="A-", width=30, height=24,
            command=lambda: self.zoom.editor_out() or self._update_editor_zoom_label(),
            font=self.ui_font).pack(side="right", padx=2)
        
        self.editor = ctk.CTkTextbox(self.editor_frame, wrap="word", 
            font=("Consolas", EDITOR_FONT_SIZE), undo=True)
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.find_bar = FindReplaceBar(self.editor_frame, self.editor, on_close=self._on_find_close)
        self._create_context_menu()
        
        # Preview panel
        self.preview_frame = ctk.CTkFrame(self.paned)
        self.paned.add(self.preview_frame, minsize=150, stretch="always")
        
        ph = ctk.CTkFrame(self.preview_frame, height=35)
        ph.pack(fill="x")
        
        self.preview_collapse_btn = ctk.CTkButton(
            ph, text="◀", width=25, height=24,
            command=self._toggle_editor_collapse, font=self.ui_font
        )
        self.preview_collapse_btn.pack(side="left", padx=5)
        
        self.preview_title_label = ctk.CTkLabel(ph, text=t("panel.preview"), font=self.ui_font_bold)
        self.preview_title_label.pack(side="left", padx=5)
        
        # Frozen controls
        ff = ctk.CTkFrame(ph, fg_color="transparent")
        ff.pack(side="left", padx=10)
        
        self.preview_frozen = ctk.BooleanVar(value=False)
        self.frozen_checkbox = ctk.CTkCheckBox(ff, text="❄️", width=24, height=24,
            variable=self.preview_frozen, command=self._on_frozen_toggle,
            font=("Segoe UI Emoji", 14), checkbox_width=20, checkbox_height=20)
        self.frozen_checkbox.pack(side="left", padx=2)
        self.tooltip_mgr.add_tooltip(self.frozen_checkbox, "tooltip.frozen")
        
        self.update_btn = ctk.CTkButton(ff, text="🔄", width=30, height=24,
            command=self._force_update_preview, font=("Segoe UI Emoji", 14))
        self.update_btn.pack(side="left", padx=2)
        self.tooltip_mgr.add_tooltip(self.update_btn, "tooltip.refresh_preview")
        
        # Preview zoom
        zf = ctk.CTkFrame(ph, fg_color="transparent")
        zf.pack(side="right", padx=5)
        
        ctk.CTkButton(zf, text="A+", width=30, height=24,
            command=self._preview_zoom_in, font=self.ui_font).pack(side="right", padx=2)
        self.zoom_label = ctk.CTkLabel(zf, text="16px", font=self.ui_font, width=40)
        self.zoom_label.pack(side="right", padx=2)
        ctk.CTkButton(zf, text="A-", width=30, height=24,
            command=self._preview_zoom_out, font=self.ui_font).pack(side="right", padx=2)
        
        pc = ctk.CTkFrame(self.preview_frame)
        pc.pack(fill="both", expand=True, padx=5, pady=5)
        
        if HTMLFRAME_AVAILABLE:
            self.preview = HtmlFrame(pc, messages_enabled=False)
        else:
            self.preview = ctk.CTkTextbox(pc, wrap="word")
        self.preview.pack(fill="both", expand=True)
    
    def _create_context_menu(self):
        """Create right-click menu"""
        if hasattr(self, 'ctx_menu') and self.ctx_menu:
            try:
                self.ctx_menu.destroy()
            except:
                pass
        
        self.ctx_menu = Menu(self.editor, tearoff=0)
        self.ctx_menu.add_command(label=t("menu.undo"), command=self._undo, accelerator="Ctrl+Z")
        self.ctx_menu.add_command(label=t("menu.redo"), command=self._redo, accelerator="Ctrl+Y")
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label=t("menu.cut"), command=self._cut, accelerator="Ctrl+X")
        self.ctx_menu.add_command(label=t("menu.copy"), command=self._copy, accelerator="Ctrl+C")
        self.ctx_menu.add_command(label=t("menu.paste"), command=self._paste, accelerator="Ctrl+V")
        self.ctx_menu.add_separator()
        
        snippets_menu = Menu(self.ctx_menu, tearoff=0)
        self.ctx_menu.add_cascade(label=t("menu.insert_snippet"), menu=snippets_menu)
        
        for label, snippet in get_snippets().items():
            if snippet is None:
                snippets_menu.add_separator()
            else:
                snippets_menu.add_command(label=label, command=lambda s=snippet: self._insert(s))
        
        self.editor.bind("<Button-3>", lambda e: self.ctx_menu.tk_popup(e.x_root, e.y_root))
    
    def _create_status_bar(self):
        """Create status bar"""
        sb = ctk.CTkFrame(self, height=30)
        sb.pack(fill="x", padx=5, pady=(0, 5))
        
        self.status_label = ctk.CTkLabel(sb, text=t("status.ready"), anchor="w", font=self.ui_font)
        self.status_label.pack(side="left", padx=10)
        self.file_label = ctk.CTkLabel(sb, text=t("status.no_file"), anchor="e", font=self.ui_font)
        self.file_label.pack(side="right", padx=10)
    
    def _update_status_dnd(self):
        """Update status with DnD info"""
        if self.dnd_enabled:
            self.status_label.configure(text=t("status.drag_hint"))
    
    # =========================================================================
    # BINDINGS
    # =========================================================================
    
    def _setup_bindings(self):
        """Setup keyboard shortcuts"""
        self.bind("<Control-n>", lambda e: self._new())
        self.bind("<Control-o>", lambda e: self._open())
        self.bind("<Control-s>", lambda e: self._save())
        self.bind("<Control-Shift-s>", lambda e: self._save_as())
        self.bind("<Control-Shift-S>", lambda e: self._save_as())
        self.bind("<Control-z>", lambda e: self._undo())
        self.bind("<Control-y>", lambda e: self._redo())
        self.bind("<Control-plus>", lambda e: (self.zoom.editor_in(), self._update_editor_zoom_label()))
        self.bind("<Control-minus>", lambda e: (self.zoom.editor_out(), self._update_editor_zoom_label()))
        self.bind("<Control-0>", lambda e: (self.zoom.editor_reset(), self._update_editor_zoom_label()))
        self.bind("<Control-f>", lambda e: self._show_find())
        self.bind("<Control-h>", lambda e: self._show_replace())
        self.bind("<F3>", lambda e: self._find_next())
        self.bind("<Shift-F3>", lambda e: self._find_prev())
        self.bind("<Escape>", lambda e: self._close_find())
        self.editor.bind("<Control-MouseWheel>", self._on_editor_wheel)
        self.editor.bind("<KeyRelease>", lambda e: self._on_edit())
    
    def _on_editor_wheel(self, e):
        """Handle Ctrl+wheel zoom"""
        self.zoom.editor_in() if e.delta > 0 else self.zoom.editor_out()
        self._update_editor_zoom_label()
        return "break"
    
    def _update_editor_zoom_label(self):
        self.editor_zoom_label.configure(text=f"{self.zoom.editor_size}px")
    
    def _preview_zoom_in(self):
        if self.zoom.preview_in():
            self.zoom_label.configure(text=self.zoom.get_preview_zoom_text())
            self._force_update_preview()
    
    def _preview_zoom_out(self):
        if self.zoom.preview_out():
            self.zoom_label.configure(text=self.zoom.get_preview_zoom_text())
            self._force_update_preview()
    
    def _on_edit(self):
        self._schedule_update()
        self._update_title()
    
    # =========================================================================
    # EDIT ACTIONS
    # =========================================================================
    
    def _undo(self):
        self.editor.focus_set()
        try:
            self.editor.edit_undo()
            self._on_edit()
        except:
            pass
    
    def _redo(self):
        self.editor.focus_set()
        try:
            self.editor.edit_redo()
            self._on_edit()
        except:
            pass
    
    def _cut(self):
        try:
            sel = self.editor.get("sel.first", "sel.last")
            if sel:
                self.clipboard_clear()
                self.clipboard_append(sel)
                self.editor.delete("sel.first", "sel.last")
                self._on_edit()
        except:
            pass
    
    def _copy(self):
        try:
            sel = self.editor.get("sel.first", "sel.last")
            if sel:
                self.clipboard_clear()
                self.clipboard_append(sel)
        except:
            pass
    
    def _paste(self):
        try:
            text = self.clipboard_get()
            if text:
                try:
                    self.editor.delete("sel.first", "sel.last")
                except:
                    pass
                self.editor.insert("insert", text)
                self._on_edit()
        except:
            pass
    
    # =========================================================================
    # FIND / REPLACE
    # =========================================================================
    
    def _show_find(self):
        self.find_bar.show(with_replace=False)
        return "break"
    
    def _show_replace(self):
        self.find_bar.show(with_replace=True)
        return "break"
    
    def _find_next(self):
        if self.find_bar.is_visible():
            self.find_bar._find_next()
        return "break"
    
    def _find_prev(self):
        if self.find_bar.is_visible():
            self.find_bar._find_prev()
        return "break"
    
    def _close_find(self):
        if self.find_bar.is_visible():
            self.find_bar.hide()
            return "break"
    
    def _on_find_close(self):
        self.editor.focus_set()
    
    # =========================================================================
    # FILE ACTIONS
    # =========================================================================
    
    def _new(self):
        if self.file_mgr.new(get_example_document()):
            self._schedule_update()
    
    def _open(self):
        if self.file_mgr.open():
            self._update_recent_menu()
            self._schedule_update()
    
    def _save(self):
        if self.file_mgr.save():
            self._update_recent_menu()
        self._update_title()
    
    def _save_as(self):
        if self.file_mgr.save_as():
            self._update_recent_menu()
        self._update_title()
    
    def _open_recent(self, filepath):
        """Open a recent file"""
        if not os.path.exists(filepath):
            if messagebox.askyesno(
                t("dialog.file_not_found"),
                t("dialog.file_not_found_msg", filepath=filepath)
            ):
                remove_recent_file(filepath)
                self._update_recent_menu()
            return
        
        if not self.file_mgr.check_unsaved():
            return
        
        self.file_mgr.load(filepath)
        add_recent_file(filepath)
        self._update_recent_menu()
        self._schedule_update()
    
    def _manage_recent(self):
        """Open recent files manager"""
        self.recent_mgr.show()
    
    def _on_drop(self, path):
        if not self.file_mgr.is_valid_extension(path):
            messagebox.showwarning(t("dialog.error"), t("dialog.error_extension"))
            return
        if self.file_mgr.check_unsaved():
            if self.file_mgr.load(path):
                self._update_recent_menu()
            self._schedule_update()
    
    def _insert(self, snippet):
        self.editor.insert("insert", snippet)
        self._schedule_update()
    
    def _on_file_change(self, filepath, content):
        self.file_label.configure(text=self.file_mgr.get_filename())
        self._update_title()
    
    def _update_title(self):
        dirty = " *" if self.file_mgr.is_dirty() else ""
        name = self.file_mgr.get_filename()
        self.title(f"{APP_NAME} v{APP_VERSION} - {name}{dirty}")
    
    def _on_close(self):
        if self.file_mgr.check_unsaved():
            self.destroy()
    
    # =========================================================================
    # PREVIEW
    # =========================================================================
    
    def _schedule_update(self):
        if self.preview_frozen.get():
            return
        if self.update_job:
            self.after_cancel(self.update_job)
        self.update_job = self.after(300, self._update_preview)
    
    def _update_preview(self):
        md = self.editor.get("1.0", "end-1c")
        zoom_css = self.zoom.get_zoom_css()
        html = render_full_html(md, self.current_style, zoom_css)
        
        try:
            if HTMLFRAME_AVAILABLE:
                self.preview.load_html(html)
            else:
                self.preview.delete("1.0", "end")
                self.preview.insert("1.0", html)
        except Exception as e:
            print(f"Error preview: {e}")
    
    def _force_update_preview(self):
        if self.update_job:
            self.after_cancel(self.update_job)
        
        md = self.editor.get("1.0", "end-1c")
        zoom_css = self.zoom.get_zoom_css()
        html = render_full_html(md, self.current_style, zoom_css)
        
        try:
            if HTMLFRAME_AVAILABLE:
                scroll_pos = self._get_preview_scroll()
                self.preview.load_html(html)
                if scroll_pos is not None and scroll_pos > 0:
                    self.after(100, lambda: self._set_preview_scroll(scroll_pos))
            else:
                self.preview.delete("1.0", "end")
                self.preview.insert("1.0", html)
        except Exception as e:
            print(f"Error preview: {e}")
    
    def _get_preview_scroll(self):
        try:
            if HTMLFRAME_AVAILABLE:
                if hasattr(self.preview, 'html') and hasattr(self.preview.html, 'yview'):
                    yview = self.preview.html.yview()
                    if yview:
                        return yview[0]
                elif hasattr(self.preview, 'yview'):
                    yview = self.preview.yview()
                    if yview:
                        return yview[0]
        except:
            pass
        return 0
    
    def _set_preview_scroll(self, pos):
        try:
            if HTMLFRAME_AVAILABLE and pos is not None and pos > 0:
                try:
                    pixels = int(pos * 10000)
                    self.preview.run_javascript(f"window.scrollTo(0, {pixels});")
                except:
                    pass
                try:
                    if hasattr(self.preview, 'html') and hasattr(self.preview.html, 'yview_moveto'):
                        self.preview.html.yview_moveto(pos)
                    elif hasattr(self.preview, 'yview_moveto'):
                        self.preview.yview_moveto(pos)
                except:
                    pass
        except:
            pass
    
    def _on_frozen_toggle(self):
        from .config import update_ui_config
        update_ui_config(preview_frozen=self.preview_frozen.get())
        if not self.preview_frozen.get():
            self._schedule_update()
    
    # =========================================================================
    # STYLES
    # =========================================================================
    
    def _apply_style(self, style):
        self.current_style = style
        self.style_combo.set(style.get('name', 'Custom'))
        self._force_update_preview()
    
    def _on_style_change(self, sel):
        for f, s in self.available_styles.items():
            if s.get('name', f) == sel:
                self._apply_style(s)
                break
    
    def _edit_style(self):
        StyleEditorWindow(self, self.current_style, self._on_style_saved)
    
    def _on_style_saved(self, data, save=True):
        self.current_style = data
        if save and '_filepath' in data:
            try:
                save_style(data)
            except Exception as e:
                messagebox.showerror(t("dialog.error"), f"{t('dialog.error_save')}:\n{e}")
        self._force_update_preview()
    
    def _reload_styles(self):
        self._load_styles()
        update_styles_menu(self)
        self.style_combo.configure(values=get_style_names(self.available_styles))
        self.status_label.configure(text=t("status.styles_reloaded"))
    
    # =========================================================================
    # EXPORT
    # =========================================================================
    
    def _copy_html(self):
        md = self.editor.get("1.0", "end-1c")
        html = render_full_html(md, self.current_style)
        open_html_in_browser(
            html, 
            suggested_name=self.file_mgr.get_base_name(),
            suggested_dir=self.file_mgr.get_directory(),
            status_callback=lambda m: self.status_label.configure(text=m)
        )
    
    def _export_pdf(self):
        md = self.editor.get("1.0", "end-1c")
        html = render_full_html(md, self.current_style)
        export_to_pdf(
            html,
            suggested_name=self.file_mgr.get_base_name(),
            suggested_dir=self.file_mgr.get_directory(),
            status_callback=lambda m: self.status_label.configure(text=m),
            update_ui_callback=self.update
        )
    
    # =========================================================================
    # PANEL COLLAPSE
    # =========================================================================
    
    def _toggle_preview_collapse(self):
        if not self.preview_expanded:
            self.paned.add(self.preview_frame, minsize=150, stretch="always")
            self.preview_expanded = True
            self.editor_collapse_btn.configure(text="▶")
            self._schedule_update()
        else:
            self.paned.forget(self.preview_frame)
            self.preview_expanded = False
            self.editor_collapse_btn.configure(text="◀")
    
    def _toggle_editor_collapse(self):
        if not self.editor_expanded:
            self.paned.add(self.editor_frame, before=self.preview_frame, minsize=150, stretch="always")
            self.editor_expanded = True
            self.preview_collapse_btn.configure(text="◀")
        else:
            self.paned.forget(self.editor_frame)
            self.editor_expanded = False
            self.preview_collapse_btn.configure(text="▶")
    
    # =========================================================================
    # THEME & LANGUAGE
    # =========================================================================
    
    def _toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.is_dark_mode.get() else "light")
    
    def _toggle_theme_btn(self):
        self.is_dark_mode.set(not self.is_dark_mode.get())
        ctk.set_appearance_mode("dark" if self.is_dark_mode.get() else "light")
        icon = "theme_light" if self.is_dark_mode.get() else "theme_dark"
        self.theme_btn.configure(text=get_icon_text(icon))
    
    def _show_language_menu(self):
        menu = Menu(self, tearoff=0)
        for code, flag, display in i18n.get_language_flag_list():
            menu.add_command(
                label=f"{flag}  {display}",
                command=lambda c=code: i18n.set_language(c)
            )
        x = self.lang_btn.winfo_rootx()
        y = self.lang_btn.winfo_rooty() + self.lang_btn.winfo_height()
        menu.tk_popup(x, y)
    
    def _show_about(self):
        msg = t("dialog.about_msg", app_name=APP_NAME, version=APP_VERSION)
        messagebox.showinfo(t("dialog.about_title"), msg)
