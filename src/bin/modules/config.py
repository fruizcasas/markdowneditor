# -*- coding: utf-8 -*-
"""
Markdown Editor - Global configuration
Configuración global: rutas, constantes, versión, configuración UI

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
import sys
import json

# =============================================================================
# VERSION
# =============================================================================

APP_NAME = "Markdown Editor"
APP_VERSION = "1.3.0"

# =============================================================================
# PATHS / RUTAS
# =============================================================================

def get_app_dir():
    """
    Get application root directory
    Obtiene directorio raíz de la aplicación
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

APP_DIR = get_app_dir()
STYLES_DIR = os.path.join(APP_DIR, "styles")
WKHTMLTOPDF_DIR = os.path.join(APP_DIR, "wkhtmltopdf")
WKHTMLTOPDF_EXE = os.path.join(WKHTMLTOPDF_DIR, "bin", "wkhtmltopdf.exe")
CONFIG_FILE = os.path.join(APP_DIR, "config.json")

# =============================================================================
# URLs
# =============================================================================

WKHTMLTOPDF_DOWNLOAD_URL = "https://wkhtmltopdf.org/downloads.html"

# =============================================================================
# UI - Default values / Valores por defecto
# =============================================================================

UI_FONT_FAMILY = "Segoe UI"
UI_FONT_SIZE = 13
UI_FONT_SIZE_SMALL = 11
UI_FONT_SIZE_HEADER = 14

# Defaults for UI state / Valores por defecto para estado UI
DEFAULT_UI_CONFIG = {
    "editor_font_size": 14,
    "preview_font_size": 16,
    "preview_frozen": False,
    "editor_collapsed": False,
    "preview_collapsed": False
}

# Shortcuts / Atajos
EDITOR_FONT_SIZE = DEFAULT_UI_CONFIG["editor_font_size"]
PREVIEW_FONT_SIZE = DEFAULT_UI_CONFIG["preview_font_size"]

# =============================================================================
# UI CONFIG - Load / Save
# =============================================================================

_ui_config = None

def _load_full_config():
    """Load full config.json / Carga config.json completo"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError, OSError):
            pass  # Return empty config on error / Retorna config vacía en error
    return {}

def _save_full_config(config):
    """Save full config.json / Guarda config.json completo"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, OSError, TypeError):
        return False

def load_ui_config():
    """
    Load UI configuration from config.json
    Carga configuración UI desde config.json
    
    Returns:
        dict: UI config with defaults applied
    """
    global _ui_config
    
    full_config = _load_full_config()
    stored_ui = full_config.get("ui", {})
    
    # Merge with defaults / Fusionar con valores por defecto
    _ui_config = DEFAULT_UI_CONFIG.copy()
    for key in DEFAULT_UI_CONFIG:
        if key in stored_ui:
            _ui_config[key] = stored_ui[key]
    
    return _ui_config

def save_ui_config(ui_config):
    """
    Save UI configuration to config.json
    Guarda configuración UI en config.json
    
    Args:
        ui_config: dict with UI settings
    """
    global _ui_config
    _ui_config = ui_config
    
    full_config = _load_full_config()
    full_config["ui"] = ui_config
    _save_full_config(full_config)

def get_ui_config():
    """
    Get current UI config (load if not loaded)
    Obtiene config UI actual (carga si no está cargada)
    """
    global _ui_config
    if _ui_config is None:
        load_ui_config()
    return _ui_config

def update_ui_config(**kwargs):
    """
    Update specific UI config values and save
    Actualiza valores específicos de config UI y guarda
    
    Example: update_ui_config(editor_font_size=16, preview_frozen=True)
    """
    config = get_ui_config()
    for key, value in kwargs.items():
        if key in config:
            config[key] = value
    save_ui_config(config)


# =============================================================================
# RECENT FILES - Load / Save
# =============================================================================

MAX_RECENT_FILES = 10

def get_recent_files():
    """
    Get list of recent files from config
    Obtiene lista de ficheros recientes desde config
    
    Returns:
        list: List of file paths (most recent first)
    """
    full_config = _load_full_config()
    return full_config.get("recent_files", [])


def add_recent_file(filepath):
    """
    Add a file to recent files list
    Añade un fichero a la lista de recientes
    
    Args:
        filepath: Full path to the file
    """
    if not filepath:
        return
    
    # Normalize path / Normalizar ruta
    filepath = os.path.normpath(filepath)
    
    full_config = _load_full_config()
    recent = full_config.get("recent_files", [])
    
    # Remove if already exists (will re-add at top)
    # Quitar si ya existe (se re-añadirá arriba)
    if filepath in recent:
        recent.remove(filepath)
    
    # Add at beginning / Añadir al principio
    recent.insert(0, filepath)
    
    # Keep only MAX / Mantener solo MAX
    recent = recent[:MAX_RECENT_FILES]
    
    full_config["recent_files"] = recent
    _save_full_config(full_config)


def remove_recent_file(filepath):
    """
    Remove a file from recent files list
    Elimina un fichero de la lista de recientes
    
    Args:
        filepath: Full path to the file
    """
    filepath = os.path.normpath(filepath)
    
    full_config = _load_full_config()
    recent = full_config.get("recent_files", [])
    
    if filepath in recent:
        recent.remove(filepath)
        full_config["recent_files"] = recent
        _save_full_config(full_config)


def clear_recent_files():
    """
    Clear all recent files
    Limpia todos los ficheros recientes
    """
    full_config = _load_full_config()
    full_config["recent_files"] = []
    _save_full_config(full_config)
