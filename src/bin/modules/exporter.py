# -*- coding: utf-8 -*-
"""
Markdown Editor - Export functions (PDF, HTML for clipboard/Outlook)
Funciones de exportación (PDF, HTML para portapapeles/Outlook)

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
import subprocess
import tempfile
import webbrowser
from tkinter import messagebox, filedialog

from .config import WKHTMLTOPDF_EXE, WKHTMLTOPDF_DIR, WKHTMLTOPDF_DOWNLOAD_URL
from .i18n import t


def is_wkhtmltopdf_available():
    """Check if wkhtmltopdf is available"""
    return os.path.exists(WKHTMLTOPDF_EXE)


def _get_unique_filepath(directory, base_name, extension):
    """Get unique filepath, adding (1), (2), etc. if file exists."""
    filepath = os.path.join(directory, f"{base_name}{extension}")
    if not os.path.exists(filepath):
        return filepath
    
    counter = 1
    while True:
        filepath = os.path.join(directory, f"{base_name} ({counter}){extension}")
        if not os.path.exists(filepath):
            return filepath
        counter += 1


def open_html_in_browser(html_content, suggested_name=None, suggested_dir=None, status_callback=None):
    """
    Save HTML and open in browser for copy/paste to Outlook.
    
    Args:
        html_content: HTML string to display
        suggested_name: Base name for file
        suggested_dir: Directory to save
        status_callback: Function to update status bar
    """
    try:
        base_name = suggested_name or "document"
        
        if suggested_dir and os.path.isdir(suggested_dir):
            save_dir = suggested_dir
        else:
            save_dir = tempfile.gettempdir()
        
        filepath = _get_unique_filepath(save_dir, base_name, ".html")
        filename = os.path.basename(filepath)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        webbrowser.open(f"file://{filepath}")
        
        if status_callback:
            status_callback(f"{t('status.html_exported')}: {filename}")
        
        messagebox.showinfo(
            t("dialog.copy_html_title"),
            t("dialog.copy_html_instructions", filename=filename)
        )
        return True
        
    except Exception as e:
        messagebox.showerror(t("dialog.error"), f"Error:\n{e}")
        return False


def export_to_pdf(html_content, suggested_name=None, suggested_dir=None, 
                  status_callback=None, update_ui_callback=None):
    """
    Export HTML to PDF using wkhtmltopdf.
    
    Args:
        html_content: HTML string to convert
        suggested_name: Suggested filename without extension
        suggested_dir: Suggested directory
        status_callback: Function to update status bar
        update_ui_callback: Function to refresh UI
    
    Returns:
        True if success, False if failed or cancelled
    """
    if not is_wkhtmltopdf_available():
        response = messagebox.askyesno(
            t("dialog.wkhtmltopdf_title"),
            t("dialog.wkhtmltopdf_msg")
        )
        if response:
            _prompt_wkhtmltopdf_download()
        return False
    
    initial_file = f"{suggested_name}.pdf" if suggested_name else "document.pdf"
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialdir=suggested_dir,
        initialfile=initial_file
    )
    if not filepath:
        return False
    
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.html',
            delete=False, encoding='utf-8'
        ) as f:
            f.write(html_content)
            temp_html = f.name
        
        if status_callback:
            status_callback(t("status.generating_pdf"))
        if update_ui_callback:
            update_ui_callback()
        
        result = subprocess.run(
            [WKHTMLTOPDF_EXE, '--encoding', 'utf-8', temp_html, filepath],
            capture_output=True,
            text=True
        )
        
        os.unlink(temp_html)
        
        if result.returncode == 0:
            filename = os.path.basename(filepath)
            if status_callback:
                status_callback(f"{t('status.pdf_exported')}: {filename}")
            
            os.startfile(filepath)
            return True
        else:
            raise Exception(result.stderr)
            
    except Exception as e:
        messagebox.showerror(t("dialog.error"), f"Error:\n{e}")
        if status_callback:
            status_callback(t("status.error_pdf"))
        return False


def _prompt_wkhtmltopdf_download():
    """Open download page and show instructions"""
    webbrowser.open(WKHTMLTOPDF_DOWNLOAD_URL)
    
    messagebox.showinfo(
        t("dialog.download_title"),
        t("dialog.download_instructions", path=WKHTMLTOPDF_DIR)
    )
