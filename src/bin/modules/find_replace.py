# -*- coding: utf-8 -*-
"""
Markdown Editor - Find and Replace bar
Barra de buscar y reemplazar

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import customtkinter as ctk
from .i18n import t
from .config import UI_FONT_FAMILY, UI_FONT_SIZE


class FindReplaceBar(ctk.CTkFrame):
    """
    Find and Replace bar that appears above the editor
    Barra de buscar/reemplazar que aparece sobre el editor
    """
    
    def __init__(self, parent, editor_widget, on_close=None):
        """
        Initialize find bar
        
        Args:
            parent: Parent widget
            editor_widget: CTkTextbox to search in
            on_close: Callback when bar is closed
        """
        super().__init__(parent, fg_color=("gray85", "gray20"), corner_radius=0)
        
        self.editor = editor_widget
        self.on_close_callback = on_close
        self.matches = []
        self.current_match = -1
        self.case_sensitive = ctk.BooleanVar(value=False)
        self.show_replace = False
        
        # Tag for highlighting / Tag para resaltado
        self.highlight_tag = "find_highlight"
        self.current_tag = "find_current"
        
        self._create_ui()
        self._setup_bindings()
    
    def _create_ui(self):
        """Create UI elements"""
        font = (UI_FONT_FAMILY, UI_FONT_SIZE)
        
        # Main container
        self.main_row = ctk.CTkFrame(self, fg_color="transparent")
        self.main_row.pack(fill="x", padx=5, pady=5)
        
        # Find entry
        self.find_entry = ctk.CTkEntry(
            self.main_row, width=250, height=28,
            placeholder_text=t("find.placeholder"),
            font=font
        )
        self.find_entry.pack(side="left", padx=(0, 5))
        
        # Counter label "3 of 15"
        self.counter_label = ctk.CTkLabel(
            self.main_row, text="", width=70,
            font=(UI_FONT_FAMILY, UI_FONT_SIZE - 1)
        )
        self.counter_label.pack(side="left", padx=5)
        
        # Navigation buttons
        btn_cfg = {"width": 28, "height": 28, "font": font}
        
        self.prev_btn = ctk.CTkButton(
            self.main_row, text="▲", command=self._find_prev, **btn_cfg
        )
        self.prev_btn.pack(side="left", padx=1)
        
        self.next_btn = ctk.CTkButton(
            self.main_row, text="▼", command=self._find_next, **btn_cfg
        )
        self.next_btn.pack(side="left", padx=1)
        
        # Case sensitive toggle
        self.case_btn = ctk.CTkButton(
            self.main_row, text=t("find.case_sensitive"), width=32, height=28,
            font=font, fg_color="transparent",
            hover_color=("gray75", "gray35"),
            command=self._toggle_case
        )
        self.case_btn.pack(side="left", padx=(10, 5))
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self.main_row, text="✕", width=28, height=28,
            font=font, fg_color="transparent",
            hover_color=("gray75", "gray35"),
            command=self.hide
        )
        self.close_btn.pack(side="right", padx=5)
        
        # Replace row (hidden by default)
        self.replace_row = ctk.CTkFrame(self, fg_color="transparent")
        
        self.replace_entry = ctk.CTkEntry(
            self.replace_row, width=250, height=28,
            placeholder_text=t("find.replace_placeholder"),
            font=font
        )
        self.replace_entry.pack(side="left", padx=(0, 5))
        
        self.replace_btn = ctk.CTkButton(
            self.replace_row, text=t("find.replace"), width=80, height=28,
            font=font, command=self._replace_current
        )
        self.replace_btn.pack(side="left", padx=2)
        
        self.replace_all_btn = ctk.CTkButton(
            self.replace_row, text=t("find.replace_all"), width=60, height=28,
            font=font, command=self._replace_all
        )
        self.replace_all_btn.pack(side="left", padx=2)
    
    def _setup_bindings(self):
        """Setup keyboard bindings"""
        self.find_entry.bind("<Return>", lambda e: self._find_next())
        self.find_entry.bind("<Shift-Return>", lambda e: self._find_prev())
        self.find_entry.bind("<Escape>", lambda e: self.hide())
        self.find_entry.bind("<KeyRelease>", lambda e: self._on_search_change())
        
        self.replace_entry.bind("<Return>", lambda e: self._replace_current())
        self.replace_entry.bind("<Escape>", lambda e: self.hide())
    
    def show(self, with_replace=False):
        """Show the find bar"""
        self.show_replace = with_replace
        
        if with_replace:
            self.replace_row.pack(fill="x", padx=5, pady=(0, 5))
        else:
            self.replace_row.pack_forget()
        
        self.pack(fill="x", before=self.editor)
        self.find_entry.focus_set()
        
        # Select all text in entry if any
        self.find_entry.select_range(0, "end")
        
        # If there's selected text in editor, use it as search term
        try:
            sel = self.editor.get("sel.first", "sel.last")
            if sel and "\n" not in sel:
                self.find_entry.delete(0, "end")
                self.find_entry.insert(0, sel)
                self.find_entry.select_range(0, "end")
                self._do_search()
        except:
            pass
    
    def hide(self):
        """Hide the find bar and clear highlights"""
        self._clear_highlights()
        self.pack_forget()
        self.editor.focus_set()
        
        if self.on_close_callback:
            self.on_close_callback()
    
    def is_visible(self):
        """Check if bar is visible"""
        return self.winfo_ismapped()
    
    def _toggle_case(self):
        """Toggle case sensitive search"""
        self.case_sensitive.set(not self.case_sensitive.get())
        
        # Update button appearance
        if self.case_sensitive.get():
            self.case_btn.configure(fg_color=("gray70", "gray40"))
        else:
            self.case_btn.configure(fg_color="transparent")
        
        self._do_search()
    
    def _on_search_change(self):
        """Called when search text changes"""
        self._do_search()
    
    def _do_search(self):
        """Execute search and highlight matches"""
        self._clear_highlights()
        self.matches = []
        self.current_match = -1
        
        query = self.find_entry.get()
        if not query:
            self._update_counter()
            return
        
        # Get editor content
        content = self.editor.get("1.0", "end-1c")
        
        # Search
        if not self.case_sensitive.get():
            search_content = content.lower()
            search_query = query.lower()
        else:
            search_content = content
            search_query = query
        
        # Find all matches
        start = 0
        while True:
            pos = search_content.find(search_query, start)
            if pos == -1:
                break
            
            # Convert to line.char format
            line = content[:pos].count("\n") + 1
            col = pos - content[:pos].rfind("\n") - 1
            start_idx = f"{line}.{col}"
            end_idx = f"{line}.{col + len(query)}"
            
            self.matches.append((start_idx, end_idx))
            start = pos + 1
        
        # Highlight all matches
        self._configure_tags()
        for start_idx, end_idx in self.matches:
            self.editor._textbox.tag_add(self.highlight_tag, start_idx, end_idx)
        
        # Go to first match
        if self.matches:
            self.current_match = 0
            self._highlight_current()
        
        self._update_counter()
    
    def _configure_tags(self):
        """Configure highlight tags"""
        # All matches - yellow background
        self.editor._textbox.tag_configure(
            self.highlight_tag,
            background="#FFFF00",
            foreground="#000000"
        )
        # Current match - orange background
        self.editor._textbox.tag_configure(
            self.current_tag,
            background="#FF8C00",
            foreground="#000000"
        )
        # Current tag should be on top
        self.editor._textbox.tag_raise(self.current_tag)
    
    def _clear_highlights(self):
        """Clear all highlight tags"""
        try:
            self.editor._textbox.tag_remove(self.highlight_tag, "1.0", "end")
            self.editor._textbox.tag_remove(self.current_tag, "1.0", "end")
        except:
            pass
    
    def _highlight_current(self):
        """Highlight current match and scroll to it"""
        if not self.matches or self.current_match < 0:
            return
        
        # Remove previous current highlight
        self.editor._textbox.tag_remove(self.current_tag, "1.0", "end")
        
        # Add current highlight
        start_idx, end_idx = self.matches[self.current_match]
        self.editor._textbox.tag_add(self.current_tag, start_idx, end_idx)
        
        # Scroll to match
        self.editor._textbox.see(start_idx)
        
        # Move cursor
        self.editor._textbox.mark_set("insert", start_idx)
    
    def _update_counter(self):
        """Update the counter label"""
        if not self.matches:
            query = self.find_entry.get()
            if query:
                self.counter_label.configure(text=t("find.no_results"))
            else:
                self.counter_label.configure(text="")
        else:
            text = t("find.count", current=self.current_match + 1, total=len(self.matches))
            self.counter_label.configure(text=text)
    
    def _find_next(self):
        """Go to next match"""
        if not self.matches:
            return
        
        self.current_match = (self.current_match + 1) % len(self.matches)
        self._highlight_current()
        self._update_counter()
    
    def _find_prev(self):
        """Go to previous match"""
        if not self.matches:
            return
        
        self.current_match = (self.current_match - 1) % len(self.matches)
        self._highlight_current()
        self._update_counter()
    
    def _replace_current(self):
        """Replace current match"""
        if not self.matches or self.current_match < 0:
            return
        
        start_idx, end_idx = self.matches[self.current_match]
        replacement = self.replace_entry.get()
        
        # Delete and insert
        self.editor._textbox.delete(start_idx, end_idx)
        self.editor._textbox.insert(start_idx, replacement)
        
        # Re-search
        self._do_search()
        
        # Go to next match if any
        if self.matches and self.current_match >= len(self.matches):
            self.current_match = 0
        self._highlight_current()
        self._update_counter()
    
    def _replace_all(self):
        """Replace all matches"""
        if not self.matches:
            return
        
        query = self.find_entry.get()
        replacement = self.replace_entry.get()
        
        # Get content
        content = self.editor.get("1.0", "end-1c")
        
        # Replace
        if self.case_sensitive.get():
            new_content = content.replace(query, replacement)
        else:
            # Case insensitive replace
            import re
            new_content = re.sub(re.escape(query), replacement, content, flags=re.IGNORECASE)
        
        # Update editor
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", new_content)
        
        # Re-search
        self._do_search()
