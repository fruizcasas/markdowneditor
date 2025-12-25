# -*- coding: utf-8 -*-
"""
Markdown Editor - CSS style editor window
Ventana de edición de estilos CSS

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import json
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from .config import STYLES_DIR
from .i18n import t


class StyleEditorWindow(ctk.CTkToplevel):
    """Window for editing CSS styles"""
    
    # Basic mode properties (CSS property -> i18n key)
    BASIC_PROPERTIES = [
        ("font-family", "font_family", "combo", [
            "Segoe UI, Arial, sans-serif",
            "Calibri, Arial, sans-serif",
            "Georgia, Times New Roman, serif",
            "Consolas, Monaco, monospace",
            "Arial, sans-serif",
            "Verdana, sans-serif"
        ]),
        ("font-size", "font_size", "entry", None),
        ("color", "color", "color", None),
        ("background-color", "background_color", "color", None),
    ]
    
    # Advanced mode properties
    ADVANCED_PROPERTIES = [
        ("font-weight", "font_weight", "combo", ["normal", "bold", "600", "700"]),
        ("font-style", "font_style", "combo", ["normal", "italic"]),
        ("line-height", "line_height", "entry", None),
        ("margin-top", "margin_top", "entry", None),
        ("margin-bottom", "margin_bottom", "entry", None),
        ("padding", "padding", "entry", None),
        ("padding-left", "padding_left", "entry", None),
        ("border", "border", "entry", None),
        ("border-bottom", "border_bottom", "entry", None),
        ("border-left", "border_left", "entry", None),
        ("border-radius", "border_radius", "entry", None),
        ("text-align", "text_align", "combo", ["left", "center", "right", "justify"]),
        ("text-decoration", "text_decoration", "combo", ["none", "underline", "line-through"]),
    ]
    
    # Editable elements (CSS selector -> i18n key)
    ELEMENTS = [
        ("body", "body"),
        ("h1", "h1"),
        ("h2", "h2"),
        ("h3", "h3"),
        ("p", "p"),
        ("ul", "ul"),
        ("ol", "ol"),
        ("li", "li"),
        ("table", "table"),
        ("th", "th"),
        ("td", "td"),
        ("code", "code"),
        ("pre", "pre"),
        ("blockquote", "blockquote"),
        ("a", "a"),
        ("hr", "hr"),
        (".callout-note", "callout_note"),
        (".callout-warning", "callout_warning"),
        (".callout-important", "callout_important"),
    ]
    
    def __init__(self, parent, current_style: dict, on_save_callback):
        """Initialize style editor"""
        super().__init__(parent)
        self.title(t("style_editor.title"))
        self.geometry("800x700")
        self.transient(parent)
        self.grab_set()
        
        # Center relative to parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 800) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 700) // 2
        self.geometry(f"800x700+{x}+{y}")
        
        self.style_data = json.loads(json.dumps(current_style))
        self.on_save_callback = on_save_callback
        self.current_element = "body"
        self.advanced_mode = ctk.BooleanVar(value=False)
        self.property_widgets = {}
        
        self._create_ui()
        self._load_element_values()
        
    def _create_ui(self):
        """Create UI elements"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header_frame, text=t("style_editor.profile_name")).pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(header_frame, width=200)
        self.name_entry.pack(side="left", padx=5)
        self.name_entry.insert(0, self.style_data.get("name", t("style_editor.new_profile")))
        
        self.mode_switch = ctk.CTkSwitch(
            header_frame, text=t("style_editor.advanced_mode"),
            variable=self.advanced_mode,
            command=self._toggle_mode
        )
        self.mode_switch.pack(side="right", padx=10)
        
        # Left panel: element list
        left_panel = ctk.CTkFrame(main_frame, width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(left_panel, text=t("style_editor.elements"), font=("", 14, "bold")).pack(pady=5)
        
        self.elements_frame = ctk.CTkScrollableFrame(left_panel)
        self.elements_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.element_buttons = {}
        for element_id, element_key in self.ELEMENTS:
            btn = ctk.CTkButton(
                self.elements_frame, text=t(f"style_editor.element.{element_key}"),
                command=lambda e=element_id: self._select_element(e),
                fg_color="transparent", text_color=("gray10", "gray90"),
                anchor="w"
            )
            btn.pack(fill="x", pady=1)
            self.element_buttons[element_id] = btn
        
        # Right panel: properties
        right_panel = ctk.CTkFrame(main_frame)
        right_panel.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(right_panel, text=t("style_editor.properties"), font=("", 14, "bold")).pack(pady=5)
        
        self.properties_frame = ctk.CTkScrollableFrame(right_panel)
        self.properties_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._create_property_widgets()
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(buttons_frame, text=t("style_editor.save_profile"),
                     command=self._save_profile).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text=t("style_editor.save_as_new"),
                     command=self._save_as_new).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text=t("style_editor.apply"),
                     command=self._apply_changes).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text=t("style_editor.cancel"),
                     command=self.destroy).pack(side="right", padx=5)
        
        self._highlight_element("body")
    
    def _create_property_widgets(self):
        """Create property widgets"""
        for widget in self.properties_frame.winfo_children():
            widget.destroy()
        self.property_widgets.clear()
        
        self._create_section(self.BASIC_PROPERTIES)
        
        if self.advanced_mode.get():
            self._create_section(self.ADVANCED_PROPERTIES)
    
    def _create_section(self, properties, parent=None):
        """Create a property section"""
        if parent is None:
            parent = self.properties_frame
            
        for prop_id, prop_key, prop_type, prop_options in properties:
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", pady=3)
            
            label_text = t(f"style_editor.property.{prop_key}")
            ctk.CTkLabel(frame, text=label_text, width=120, anchor="w").pack(side="left")
            
            if prop_type == "entry":
                widget = ctk.CTkEntry(frame, width=200)
                widget.pack(side="left", padx=5)
                widget.bind("<KeyRelease>", lambda e, p=prop_id: self._on_property_change(p))
                
            elif prop_type == "combo":
                widget = ctk.CTkComboBox(frame, width=200, values=prop_options)
                widget.pack(side="left", padx=5)
                widget.configure(command=lambda v, p=prop_id: self._on_property_change(p))
                
            elif prop_type == "color":
                widget = ctk.CTkEntry(frame, width=150)
                widget.pack(side="left", padx=5)
                widget.bind("<KeyRelease>", lambda e, p=prop_id: self._on_property_change(p))
                
                color_btn = ctk.CTkButton(
                    frame, text="...", width=30,
                    command=lambda w=widget, p=prop_id: self._pick_color(w, p)
                )
                color_btn.pack(side="left")
            
            self.property_widgets[prop_id] = widget
    
    def _toggle_mode(self):
        """Switch between basic and advanced mode"""
        self._create_property_widgets()
        self._load_element_values()
    
    def _select_element(self, element_id):
        """Select an element to edit"""
        self._save_current_element()
        self.current_element = element_id
        self._highlight_element(element_id)
        self._load_element_values()
    
    def _highlight_element(self, element_id):
        """Highlight selected element"""
        for eid, btn in self.element_buttons.items():
            if eid == element_id:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")
    
    def _load_element_values(self):
        """Load values for selected element"""
        css = self.style_data.get("css", {})
        element_css = css.get(self.current_element, {})
        
        for prop_id, widget in self.property_widgets.items():
            value = element_css.get(prop_id, "")
            if isinstance(widget, ctk.CTkComboBox):
                widget.set(value)
            else:
                widget.delete(0, "end")
                widget.insert(0, value)
    
    def _save_current_element(self):
        """Save values for current element"""
        if "css" not in self.style_data:
            self.style_data["css"] = {}
        if self.current_element not in self.style_data["css"]:
            self.style_data["css"][self.current_element] = {}
        
        for prop_id, widget in self.property_widgets.items():
            value = widget.get()
            
            if value:
                self.style_data["css"][self.current_element][prop_id] = value
            elif prop_id in self.style_data["css"][self.current_element]:
                del self.style_data["css"][self.current_element][prop_id]
    
    def _on_property_change(self, prop_id):
        """Called when a property changes"""
        self._save_current_element()
    
    def _pick_color(self, entry_widget, prop_id):
        """Open color picker"""
        color = colorchooser.askcolor(title=t("style_editor.select_color"))
        if color[1]:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, color[1])
            self._on_property_change(prop_id)
    
    def _apply_changes(self):
        """Apply changes without saving to file"""
        self._save_current_element()
        self.style_data["name"] = self.name_entry.get()
        self.on_save_callback(self.style_data, save_to_file=False)
        self.destroy()
    
    def _save_profile(self):
        """Save current profile"""
        self._save_current_element()
        self.style_data["name"] = self.name_entry.get()
        self.on_save_callback(self.style_data, save_to_file=True)
        self.destroy()
    
    def _save_as_new(self):
        """Save as new profile"""
        filename = filedialog.asksaveasfilename(
            initialdir=STYLES_DIR,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            self._save_current_element()
            self.style_data["name"] = self.name_entry.get()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.style_data, f, indent=4, ensure_ascii=False)
            self.on_save_callback(self.style_data, save_to_file=False)
            messagebox.showinfo(t("style_editor.saved"), f"{t('style_editor.saved_msg')}\n{filename}")
            self.destroy()
