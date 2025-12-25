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

import customtkinter as ctk
from tkinter import messagebox, Menu, PanedWindow, HORIZONTAL

from .config import (APP_NAME, APP_VERSION, UI_FONT_FAMILY, UI_FONT_SIZE, 
                     UI_FONT_SIZE_HEADER, EDITOR_FONT_SIZE)
from .snippets import MARKDOWN_SNIPPETS, EXAMPLE_DOCUMENT
from .styles import load_all_styles, save_style, get_default_style, get_style_names
from .style_editor import StyleEditorWindow
from .renderer import render_full_html
from .exporter import open_html_in_browser, export_to_pdf
from .dnd_support import setup_window_drop, DND_AVAILABLE
from .zoom import ZoomManager
from .file_ops import FileManager
from .icons import get_icon_text, icons_available, init_icons
from .find_replace import FindReplaceBar
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
        
        # Initialize i18n FIRST / Inicializar i18n PRIMERO
        i18n.init()
        i18n.on_language_change(self._on_language_change)
        
        # Initialize icon system / Inicializar sistema de iconos
        init_icons(self)
        
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1400x900")
        
        self.is_dark_mode = ctk.BooleanVar(value=True)
        self.update_job = None
        self.current_style = None
        self.available_styles = {}
        
        # UI fonts / Fuentes UI
        self.ui_font = (UI_FONT_FAMILY, UI_FONT_SIZE)
        self.ui_font_bold = (UI_FONT_FAMILY, UI_FONT_SIZE_HEADER, "bold")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._load_styles()
        self._init_tooltip_system()
        self._create_ui()
        self._setup_managers()
        self._setup_bindings()
        
        # DnD - setup AFTER creating UI
        self.dnd_enabled = setup_window_drop(self, self._on_drop)
        
        self._init_document()
        self._update_status_dnd()
    
    def _load_styles(self):
        """Load available CSS styles / Carga estilos CSS disponibles"""
        self.available_styles = load_all_styles()
        for name in ['gitlab.json', 'default.json']:
            if name in self.available_styles:
                self.current_style = self.available_styles[name]
                break
        if not self.current_style:
            self.current_style = get_default_style()
    
    def _create_ui(self):
        """Create all UI elements / Crea todos los elementos UI"""
        self._create_menu()
        self._create_toolbar()
        self._create_main_area()
        self._create_status_bar()
    
    def _setup_managers(self):
        """Initialize zoom and file managers / Inicializa gestores de zoom y archivos"""
        from .config import get_ui_config
        
        self.zoom = ZoomManager(self.editor, lambda m: self.status_label.configure(text=m))
        self.file_mgr = FileManager(
            self.editor,
            on_file_change=self._on_file_change,
            on_status=lambda m: self.status_label.configure(text=m)
        )
        
        # Load UI state from config / Cargar estado UI desde config
        ui_config = get_ui_config()
        
        # Apply preview zoom label / Aplicar etiqueta de zoom preview
        self.zoom_label.configure(text=self.zoom.get_preview_zoom_text())
        
        # Apply editor zoom label / Aplicar etiqueta de zoom editor
        self.editor_zoom_label.configure(text=f"{self.zoom.editor_size}px")
        
        # Load frozen state / Cargar estado congelado
        self.preview_frozen.set(ui_config.get("preview_frozen", False))
    
    def _init_document(self):
        """Load example document / Carga documento de ejemplo"""
        self.editor.insert("1.0", EXAMPLE_DOCUMENT)
        self.file_mgr.mark_saved(EXAMPLE_DOCUMENT)
        self.file_label.configure(text=self.file_mgr.get_filename())
        self._update_title()
        self._schedule_update()
    
    # =========================================================================
    # LANGUAGE CHANGE - HOT RELOAD
    # =========================================================================
    
    def _on_language_change(self):
        """Rebuild UI when language changes / Reconstruye UI al cambiar idioma"""
        # Save current state / Guardar estado actual
        editor_content = self.editor.get("1.0", "end-1c")
        cursor_pos = self.editor.index("insert")
        
        # Destroy and recreate menus / Destruir y recrear menús
        self.menu_bar.destroy()
        self._create_menu()
        
        # Update toolbar labels / Actualizar etiquetas de toolbar
        self._update_toolbar_texts()
        
        # Update panel labels / Actualizar etiquetas de paneles
        self._update_panel_texts()
        
        # Update status bar / Actualizar barra de estado
        self._update_status_dnd()
        
        # Restore editor content and cursor / Restaurar contenido y cursor
        # (not needed as we don't destroy editor)
    
    def _update_toolbar_texts(self):
        """Update toolbar button tooltips / Actualiza tooltips de toolbar"""
        # Update Save As button text
        if hasattr(self, 'btn_saveas'):
            self.btn_saveas.configure(text=t("label.save_as_btn"))
        
        # Update style label
        if hasattr(self, 'style_label'):
            self.style_label.configure(text=t("label.style"))
    
    def _update_panel_texts(self):
        """Update panel header labels / Actualiza etiquetas de paneles"""
        if hasattr(self, 'editor_title_label'):
            self.editor_title_label.configure(text=t("panel.editor"))
        if hasattr(self, 'preview_title_label'):
            self.preview_title_label.configure(text=t("panel.preview"))
    
    # =========================================================================
    # MENU
    # =========================================================================
    
    def _create_menu(self):
        """Create menu bar / Crea barra de menú"""
        self.menu_bar = Menu(self)
        self.configure(menu=self.menu_bar)
        
        # File menu
        fm = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=t("menu.file"), menu=fm)
        fm.add_command(label=t("menu.new"), command=self._new, accelerator="Ctrl+N")
        fm.add_command(label=t("menu.open"), command=self._open, accelerator="Ctrl+O")
        fm.add_command(label=t("menu.save"), command=self._save, accelerator="Ctrl+S")
        fm.add_command(label=t("menu.save_as"), command=self._save_as, accelerator="Ctrl+Shift+S")
        fm.add_separator()
        fm.add_command(label=t("menu.export_pdf"), command=self._export_pdf)
        fm.add_command(label=t("menu.copy_html"), command=self._copy_html)
        fm.add_separator()
        fm.add_command(label=t("menu.exit"), command=self._on_close)
        
        # Edit menu
        em = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=t("menu.edit"), menu=em)
        em.add_command(label=t("menu.undo"), command=self._undo, accelerator="Ctrl+Z")
        em.add_command(label=t("menu.redo"), command=self._redo, accelerator="Ctrl+Y")
        em.add_separator()
        em.add_command(label=t("menu.cut"), command=self._cut, accelerator="Ctrl+X")
        em.add_command(label=t("menu.copy"), command=self._copy, accelerator="Ctrl+C")
        em.add_command(label=t("menu.paste"), command=self._paste, accelerator="Ctrl+V")
        em.add_separator()
        em.add_command(label=t("menu.find"), command=self._show_find, accelerator="Ctrl+F")
        em.add_command(label=t("menu.replace"), command=self._show_replace, accelerator="Ctrl+H")
        
        # View menu
        vm = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=t("menu.view"), menu=vm)
        vm.add_command(label=t("menu.zoom_in"), command=lambda: (self.zoom.editor_in(), self._update_editor_zoom_label()), accelerator="Ctrl++")
        vm.add_command(label=t("menu.zoom_out"), command=lambda: (self.zoom.editor_out(), self._update_editor_zoom_label()), accelerator="Ctrl+-")
        vm.add_command(label=t("menu.zoom_reset"), command=lambda: (self.zoom.editor_reset(), self._update_editor_zoom_label()), accelerator="Ctrl+0")
        vm.add_separator()
        vm.add_checkbutton(label=t("menu.dark_mode"), variable=self.is_dark_mode, command=self._toggle_theme)
        vm.add_separator()
        
        # Language submenu
        lang_menu = Menu(vm, tearoff=0)
        vm.add_cascade(label=t("menu.language"), menu=lang_menu)
        current_lang = i18n.get_current_language()
        for code, display in i18n.get_language_display_list():
            lang_menu.add_radiobutton(
                label=display,
                command=lambda c=code: i18n.set_language(c),
                value=code,
                variable=ctk.StringVar(value=current_lang)
            )
        
        # Styles menu
        self.styles_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=t("menu.styles"), menu=self.styles_menu)
        self._update_styles_menu()
        
        # Help menu
        hm = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=t("menu.help"), menu=hm)
        hm.add_command(label=t("menu.about"), command=self._show_about)
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _update_styles_menu(self):
        """Rebuild styles menu / Reconstruye menú de estilos"""
        self.styles_menu.delete(0, "end")
        for fname, style in self.available_styles.items():
            self.styles_menu.add_command(
                label=style.get('name', fname),
                command=lambda s=style: self._apply_style(s)
            )
        self.styles_menu.add_separator()
        self.styles_menu.add_command(label=t("menu.edit_style"), command=self._edit_style)
        self.styles_menu.add_command(label=t("menu.reload_styles"), command=self._reload_styles)
    
    # =========================================================================
    # TOOLBAR
    # =========================================================================
    
    def _create_toolbar(self):
        """Create toolbar with icon buttons / Crea barra de herramientas con botones de icono"""
        self.toolbar = ctk.CTkFrame(self, height=45)
        self.toolbar.pack(fill="x", padx=5, pady=5)
        
        btn_cfg = {"height": 36, "width": 44, "font": ("Segoe UI Emoji", 18),
                   "fg_color": "transparent", "hover_color": ("gray75", "gray25"),
                   "text_color": ("gray10", "gray90")}
        
        # File buttons
        self._create_icon_btn(self.toolbar, "new", self._new, "tooltip.new", btn_cfg)
        self._create_icon_btn(self.toolbar, "open", self._open, "tooltip.open", btn_cfg)
        self._create_icon_btn(self.toolbar, "save", self._save, "tooltip.save", btn_cfg)
        
        # Save As - text button
        self.btn_saveas = ctk.CTkButton(self.toolbar, text=t("label.save_as_btn"), width=50, height=36, 
                                    font=self.ui_font, fg_color="transparent",
                                    hover_color=("gray75", "gray25"),
                                    text_color=("gray10", "gray90"),
                                    command=self._save_as)
        self.btn_saveas.pack(side="left", padx=1)
        self._add_tooltip(self.btn_saveas, "tooltip.save_as")
        
        # Separator
        ctk.CTkFrame(self.toolbar, width=2, height=28, fg_color="gray50").pack(side="left", padx=8)
        
        # Edit buttons
        self._create_icon_btn(self.toolbar, "cut", self._cut, "tooltip.cut", btn_cfg)
        self._create_icon_btn(self.toolbar, "copy", self._copy, "tooltip.copy", btn_cfg)
        self._create_icon_btn(self.toolbar, "paste", self._paste, "tooltip.paste", btn_cfg)
        
        # Separator
        ctk.CTkFrame(self.toolbar, width=2, height=28, fg_color="gray50").pack(side="left", padx=8)
        
        # Undo/Redo buttons
        self._create_icon_btn(self.toolbar, "undo", self._undo, "tooltip.undo", btn_cfg)
        self._create_icon_btn(self.toolbar, "redo", self._redo, "tooltip.redo", btn_cfg)
        
        # Right side
        sf = ctk.CTkFrame(self.toolbar, fg_color="transparent")
        sf.pack(side="right", padx=5)
        
        # Export buttons
        btn_exp = {"font": self.ui_font, "height": 32}
        pdf_btn = ctk.CTkButton(sf, text="PDF", width=50, command=self._export_pdf, **btn_exp)
        pdf_btn.pack(side="right", padx=2)
        self._add_tooltip(pdf_btn, "tooltip.export_pdf")
        
        html_btn = ctk.CTkButton(sf, text="HTML", width=50, command=self._copy_html, **btn_exp)
        html_btn.pack(side="right", padx=2)
        self._add_tooltip(html_btn, "tooltip.copy_html")
        
        # Separator
        ctk.CTkFrame(sf, width=2, height=28, fg_color="gray50").pack(side="right", padx=8)
        
        # Style selector
        self.style_label = ctk.CTkLabel(sf, text=t("label.style"), font=self.ui_font)
        self.style_label.pack(side="left", padx=5)
        self.style_combo = ctk.CTkComboBox(
            sf, width=180, font=self.ui_font, height=32,
            values=get_style_names(self.available_styles),
            command=self._on_style_change,
            dropdown_font=self.ui_font
        )
        self.style_combo.pack(side="left")
        self.style_combo.set(self.current_style.get('name', 'Default'))
        ctk.CTkButton(sf, text="...", width=32, command=self._edit_style, **btn_exp).pack(side="left", padx=2)
        
        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            sf, text=get_icon_text("theme_light"), width=44, height=36,
            font=("Segoe UI Emoji", 18), fg_color="transparent",
            hover_color=("gray75", "gray25"), 
            text_color=("gray10", "gray90"),
            command=self._toggle_theme_btn
        )
        self.theme_btn.pack(side="left", padx=(10, 2))
        self._add_tooltip(self.theme_btn, "tooltip.change_theme")
    
    def _create_icon_btn(self, parent, icon_name, command, tooltip, btn_cfg, side="left"):
        """Create toolbar button with emoji icon and tooltip"""
        icon_text = get_icon_text(icon_name)
        btn = ctk.CTkButton(parent, text=icon_text, command=command, **btn_cfg)
        btn.pack(side=side, padx=1)
        self._add_tooltip(btn, tooltip)
        return btn
    
    # =========================================================================
    # TOOLTIP SYSTEM - Singleton pattern
    # =========================================================================
    
    def _init_tooltip_system(self):
        """Initialize tooltip tracking / Inicializa sistema de tooltips"""
        self._tooltip_window = None
        self._tooltip_job = None
        self._tooltip_widget = None
    
    def _add_tooltip(self, widget, key_or_text, is_key=True):
        """Add tooltip to widget / Añade tooltip al widget
        
        Args:
            widget: Widget to add tooltip to
            key_or_text: i18n key (e.g. 'tooltip.save') or plain text
            is_key: If True, key_or_text is a translation key; if False, it's plain text
        """
        widget._tt_key = key_or_text if is_key else None
        widget._tt_text = None if is_key else key_or_text
        widget.bind("<Enter>", lambda e: self._tt_schedule(widget))
        widget.bind("<Leave>", lambda e: self._tt_hide())
        widget.bind("<Button-1>", lambda e: self._tt_hide())
    
    def _tt_schedule(self, widget):
        """Schedule tooltip show after delay / Programa mostrar tooltip tras delay"""
        self._tt_hide()
        self._tooltip_widget = widget
        self._tooltip_job = self.after(400, lambda: self._tt_show(widget))
    
    def _tt_show(self, widget):
        """Show tooltip for widget / Muestra tooltip para widget"""
        if not widget.winfo_exists():
            return
        if self._tooltip_widget != widget:
            return
        
        x = widget.winfo_rootx() + widget.winfo_width() // 2
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        
        self._tooltip_window = ctk.CTkToplevel(self)
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
        
        self._tooltip_job = self.after(2500, self._tt_hide)
    
    def _tt_hide(self):
        """Hide and cleanup tooltip / Oculta y limpia tooltip"""
        if self._tooltip_job:
            try:
                self.after_cancel(self._tooltip_job)
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
    
    # =========================================================================
    # MAIN AREA
    # =========================================================================
    
    def _create_main_area(self):
        """Create split view with editor and preview / Crea vista dividida con editor y preview"""
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
        
        # Collapse button (far right) / Botón colapsar (extremo derecho)
        self.editor_collapse_btn = ctk.CTkButton(
            eh, text="▶", width=25, height=24,
            command=self._toggle_preview_collapse, font=self.ui_font
        )
        self.editor_collapse_btn.pack(side="right", padx=5)
        
        # Editor zoom controls (right side) / Controles zoom editor (derecha)
        editor_zoom_frame = ctk.CTkFrame(eh, fg_color="transparent")
        editor_zoom_frame.pack(side="right", padx=5)
        
        ctk.CTkButton(
            editor_zoom_frame, text="A+", width=30, height=24,
            command=lambda: self.zoom.editor_in() or self._update_editor_zoom_label(),
            font=self.ui_font
        ).pack(side="right", padx=2)
        self.editor_zoom_label = ctk.CTkLabel(editor_zoom_frame, text=f"{EDITOR_FONT_SIZE}px", font=self.ui_font, width=40)
        self.editor_zoom_label.pack(side="right", padx=2)
        ctk.CTkButton(
            editor_zoom_frame, text="A-", width=30, height=24,
            command=lambda: self.zoom.editor_out() or self._update_editor_zoom_label(),
            font=self.ui_font
        ).pack(side="right", padx=2)
        
        self.editor = ctk.CTkTextbox(
            self.editor_frame, wrap="word", 
            font=("Consolas", EDITOR_FONT_SIZE),
            undo=True
        )
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Find/Replace bar (initially hidden) / Barra buscar/reemplazar (oculta al inicio)
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
        
        # Frozen checkbox + Update button / Checkbox congelado + botón actualizar
        frozen_frame = ctk.CTkFrame(ph, fg_color="transparent")
        frozen_frame.pack(side="left", padx=10)
        
        self.preview_frozen = ctk.BooleanVar(value=False)
        self.frozen_checkbox = ctk.CTkCheckBox(
            frozen_frame, text="❄️", width=24, height=24,
            variable=self.preview_frozen, command=self._on_frozen_toggle,
            font=("Segoe UI Emoji", 14), checkbox_width=20, checkbox_height=20
        )
        self.frozen_checkbox.pack(side="left", padx=2)
        self._add_tooltip(self.frozen_checkbox, "tooltip.frozen")
        
        self.update_btn = ctk.CTkButton(
            frozen_frame, text="🔄", width=30, height=24,
            command=self._force_update_preview,
            font=("Segoe UI Emoji", 14)
        )
        self.update_btn.pack(side="left", padx=2)
        self._add_tooltip(self.update_btn, "tooltip.refresh_preview")
        
        # Preview zoom controls (right side) / Controles zoom preview (derecha)
        zoom_frame = ctk.CTkFrame(ph, fg_color="transparent")
        zoom_frame.pack(side="right", padx=5)
        
        ctk.CTkButton(
            zoom_frame, text="A+", width=30, height=24,
            command=self._preview_zoom_in, font=self.ui_font
        ).pack(side="right", padx=2)
        self.zoom_label = ctk.CTkLabel(zoom_frame, text="16px", font=self.ui_font, width=40)
        self.zoom_label.pack(side="right", padx=2)
        ctk.CTkButton(
            zoom_frame, text="A-", width=30, height=24,
            command=self._preview_zoom_out, font=self.ui_font
        ).pack(side="right", padx=2)
        
        pc = ctk.CTkFrame(self.preview_frame)
        pc.pack(fill="both", expand=True, padx=5, pady=5)
        
        if HTMLFRAME_AVAILABLE:
            self.preview = HtmlFrame(pc, messages_enabled=False)
        else:
            self.preview = ctk.CTkTextbox(pc, wrap="word")
        self.preview.pack(fill="both", expand=True)
    
    def _create_context_menu(self):
        """Create right-click menu with edit actions and snippets"""
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
        
        for label, snippet in MARKDOWN_SNIPPETS.items():
            if snippet is None:
                snippets_menu.add_separator()
            else:
                snippets_menu.add_command(label=label, command=lambda s=snippet: self._insert(s))
        
        self.editor.bind("<Button-3>", lambda e: self.ctx_menu.tk_popup(e.x_root, e.y_root))
    
    def _create_status_bar(self):
        """Create status bar / Crea barra de estado"""
        sb = ctk.CTkFrame(self, height=30)
        sb.pack(fill="x", padx=5, pady=(0, 5))
        
        self.status_label = ctk.CTkLabel(sb, text=t("status.ready"), anchor="w", font=self.ui_font)
        self.status_label.pack(side="left", padx=10)
        self.file_label = ctk.CTkLabel(sb, text=t("status.no_file"), anchor="e", font=self.ui_font)
        self.file_label.pack(side="right", padx=10)
    
    def _update_status_dnd(self):
        """Update status with DnD info / Actualiza status con info de DnD"""
        if self.dnd_enabled:
            self.status_label.configure(text=t("status.drag_hint"))
    
    # =========================================================================
    # BINDINGS
    # =========================================================================
    
    def _setup_bindings(self):
        """Setup keyboard shortcuts / Configura atajos de teclado"""
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
        
        # Find/Replace shortcuts / Atajos buscar/reemplazar
        self.bind("<Control-f>", lambda e: self._show_find())
        self.bind("<Control-h>", lambda e: self._show_replace())
        self.bind("<F3>", lambda e: self._find_next())
        self.bind("<Shift-F3>", lambda e: self._find_prev())
        self.bind("<Escape>", lambda e: self._close_find())
        
        self.editor.bind("<Control-MouseWheel>", self._on_editor_wheel)
        self.editor.bind("<KeyRelease>", lambda e: self._on_edit())
        
        # Note: Ctrl+MouseWheel on preview doesn't work with HtmlFrame
        # Use A-/A+ buttons instead / Usar botones A-/A+ en su lugar
    
    def _on_editor_wheel(self, e):
        """Handle Ctrl+wheel zoom on editor"""
        self.zoom.editor_in() if e.delta > 0 else self.zoom.editor_out()
        self._update_editor_zoom_label()
        return "break"
    
    def _update_editor_zoom_label(self):
        """Update editor zoom label"""
        self.editor_zoom_label.configure(text=f"{self.zoom.editor_size}px")
    
    def _preview_zoom_in(self):
        """Zoom in preview / Aumentar zoom preview"""
        if self.zoom.preview_in():
            self.zoom_label.configure(text=self.zoom.get_preview_zoom_text())
            # Force update even if frozen / Forzar update aunque esté congelado
            self._force_update_preview()
    
    def _preview_zoom_out(self):
        """Zoom out preview / Reducir zoom preview"""
        if self.zoom.preview_out():
            self.zoom_label.configure(text=self.zoom.get_preview_zoom_text())
            # Force update even if frozen / Forzar update aunque esté congelado
            self._force_update_preview()
    
    def _on_edit(self):
        """Handle text changes"""
        self._schedule_update()
        self._update_title()
    
    # =========================================================================
    # EDIT ACTIONS
    # =========================================================================
    
    def _undo(self):
        """Undo last action"""
        self.editor.focus_set()
        try:
            self.editor.edit_undo()
            self._on_edit()
        except:
            pass
    
    def _redo(self):
        """Redo last undone action"""
        self.editor.focus_set()
        try:
            self.editor.edit_redo()
            self._on_edit()
        except:
            pass
    
    def _cut(self):
        """Cut selected text"""
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
        """Copy selected text"""
        try:
            sel = self.editor.get("sel.first", "sel.last")
            if sel:
                self.clipboard_clear()
                self.clipboard_append(sel)
        except:
            pass
    
    def _paste(self):
        """Paste from clipboard"""
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
    # FIND / REPLACE - BUSCAR / REEMPLAZAR
    # =========================================================================
    
    def _show_find(self):
        """Show find bar / Mostrar barra de búsqueda"""
        self.find_bar.show(with_replace=False)
        return "break"  # Prevent default Ctrl+F behavior
    
    def _show_replace(self):
        """Show find & replace bar / Mostrar barra buscar y reemplazar"""
        self.find_bar.show(with_replace=True)
        return "break"  # Prevent default Ctrl+H behavior
    
    def _find_next(self):
        """Go to next match / Ir a siguiente coincidencia"""
        if self.find_bar.is_visible():
            self.find_bar._find_next()
        return "break"
    
    def _find_prev(self):
        """Go to previous match / Ir a coincidencia anterior"""
        if self.find_bar.is_visible():
            self.find_bar._find_prev()
        return "break"
    
    def _close_find(self):
        """Close find bar / Cerrar barra de búsqueda"""
        if self.find_bar.is_visible():
            self.find_bar.hide()
            return "break"
    
    def _on_find_close(self):
        """Called when find bar is closed / Se llama al cerrar barra de búsqueda"""
        self.editor.focus_set()
    
    # =========================================================================
    # FILE ACTIONS
    # =========================================================================
    
    def _new(self):
        """New document"""
        if self.file_mgr.new(EXAMPLE_DOCUMENT):
            self._schedule_update()
    
    def _open(self):
        """Open file"""
        if self.file_mgr.open():
            self._schedule_update()
    
    def _save(self):
        """Save file"""
        self.file_mgr.save()
        self._update_title()
    
    def _save_as(self):
        """Save as"""
        self.file_mgr.save_as()
        self._update_title()
    
    def _on_drop(self, path):
        """Handle drag & drop"""
        if not self.file_mgr.is_valid_extension(path):
            messagebox.showwarning(t("dialog.error"), t("dialog.error_extension"))
            return
        if self.file_mgr.check_unsaved():
            self.file_mgr.load(path)
            self._schedule_update()
    
    def _insert(self, snippet):
        """Insert snippet at cursor"""
        self.editor.insert("insert", snippet)
        self._schedule_update()
    
    def _on_file_change(self, filepath, content):
        """Handle file change"""
        self.file_label.configure(text=self.file_mgr.get_filename())
        self._update_title()
    
    def _update_title(self):
        """Update window title with file name and dirty flag"""
        dirty = " *" if self.file_mgr.is_dirty() else ""
        name = self.file_mgr.get_filename()
        self.title(f"{APP_NAME} v{APP_VERSION} - {name}{dirty}")
    
    def _on_close(self):
        """Handle window close"""
        if self.file_mgr.check_unsaved():
            self.destroy()
    
    # =========================================================================
    # PREVIEW
    # =========================================================================
    
    def _schedule_update(self):
        """Schedule preview update with debounce / Programa actualización con debounce"""
        # Skip if frozen / Saltar si congelado
        if self.preview_frozen.get():
            return
        
        if self.update_job:
            self.after_cancel(self.update_job)
        self.update_job = self.after(300, self._update_preview)
    
    def _update_preview(self):
        """Update preview with rendered HTML / Actualiza preview con HTML renderizado"""
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
        """Force update preview (ignore frozen) / Fuerza actualización (ignora congelado)"""
        if self.update_job:
            self.after_cancel(self.update_job)
        
        md = self.editor.get("1.0", "end-1c")
        zoom_css = self.zoom.get_zoom_css()
        html = render_full_html(md, self.current_style, zoom_css)
        
        try:
            if HTMLFRAME_AVAILABLE:
                # Get scroll position before update / Guardar scroll antes de actualizar
                scroll_pos = self._get_preview_scroll()
                
                self.preview.load_html(html)
                
                # Restore scroll after load / Restaurar scroll tras cargar
                if scroll_pos is not None and scroll_pos > 0:
                    self.after(100, lambda: self._set_preview_scroll(scroll_pos))
            else:
                self.preview.delete("1.0", "end")
                self.preview.insert("1.0", html)
        except Exception as e:
            print(f"Error preview: {e}")
    
    def _get_preview_scroll(self):
        """Get preview scroll position / Obtiene posición de scroll"""
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
        """Set preview scroll position / Establece posición de scroll"""
        try:
            if HTMLFRAME_AVAILABLE and pos is not None and pos > 0:
                # Try JavaScript
                try:
                    pixels = int(pos * 10000)
                    self.preview.run_javascript(f"window.scrollTo(0, {pixels});")
                except:
                    pass
                # Fallback to native
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
        """Handle frozen checkbox change / Maneja cambio de checkbox congelado"""
        from .config import update_ui_config
        update_ui_config(preview_frozen=self.preview_frozen.get())
        
        # If unfreezing, update preview / Si descongelamos, actualizar preview
        if not self.preview_frozen.get():
            self._schedule_update()
    
    # =========================================================================
    # STYLES
    # =========================================================================
    
    def _apply_style(self, style):
        """Apply CSS style / Aplicar estilo CSS"""
        self.current_style = style
        self.style_combo.set(style.get('name', 'Custom'))
        # Force update even if frozen / Forzar update aunque esté congelado
        self._force_update_preview()
    
    def _on_style_change(self, sel):
        """Handle style combo change"""
        for f, s in self.available_styles.items():
            if s.get('name', f) == sel:
                self._apply_style(s)
                break
    
    def _edit_style(self):
        """Open style editor"""
        StyleEditorWindow(self, self.current_style, self._on_style_saved)
    
    def _on_style_saved(self, data, save=True):
        """Handle style save / Maneja guardado de estilo"""
        self.current_style = data
        if save and '_filepath' in data:
            try:
                save_style(data)
            except Exception as e:
                messagebox.showerror(t("dialog.error"), f"{t('dialog.error_save')}:\n{e}")
        # Force update even if frozen / Forzar update aunque esté congelado
        self._force_update_preview()
    
    def _reload_styles(self):
        """Reload styles from disk"""
        self._load_styles()
        self._update_styles_menu()
        self.style_combo.configure(values=get_style_names(self.available_styles))
        self.status_label.configure(text=t("status.styles_reloaded"))
    
    # =========================================================================
    # EXPORT
    # =========================================================================
    
    def _copy_html(self):
        """Copy HTML for Outlook"""
        md = self.editor.get("1.0", "end-1c")
        html = render_full_html(md, self.current_style)
        open_html_in_browser(
            html, 
            suggested_name=self.file_mgr.get_base_name(),
            suggested_dir=self.file_mgr.get_directory(),
            status_callback=lambda m: self.status_label.configure(text=m)
        )
    
    def _export_pdf(self):
        """Export to PDF"""
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
    # PANEL COLLAPSE/RESTORE
    # =========================================================================
    
    def _toggle_preview_collapse(self):
        """Toggle preview panel"""
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
        """Toggle editor panel"""
        if not self.editor_expanded:
            self.paned.add(self.editor_frame, before=self.preview_frame, minsize=150, stretch="always")
            self.editor_expanded = True
            self.preview_collapse_btn.configure(text="◀")
        else:
            self.paned.forget(self.editor_frame)
            self.editor_expanded = False
            self.preview_collapse_btn.configure(text="▶")
    
    # =========================================================================
    # THEME
    # =========================================================================
    
    def _toggle_theme(self):
        """Toggle dark/light theme"""
        ctk.set_appearance_mode("dark" if self.is_dark_mode.get() else "light")
    
    def _toggle_theme_btn(self):
        """Toggle theme from toolbar button"""
        self.is_dark_mode.set(not self.is_dark_mode.get())
        ctk.set_appearance_mode("dark" if self.is_dark_mode.get() else "light")
        icon = "theme_light" if self.is_dark_mode.get() else "theme_dark"
        self.theme_btn.configure(text=get_icon_text(icon))
    
    def _show_about(self):
        """Show about dialog"""
        msg = t("dialog.about_msg", app_name=APP_NAME, version=APP_VERSION)
        messagebox.showinfo(t("dialog.about_title"), msg)
