# -*- coding: utf-8 -*-
"""
Internationalization module - Multi-language support
Módulo de internacionalización - Soporte multi-idioma

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import json
import os
import locale

# =============================================================================
# PATHS / RUTAS
# =============================================================================

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.dirname(os.path.dirname(_MODULE_DIR))
LANG_DIR = os.path.join(_SRC_DIR, "lang")
CONFIG_FILE = os.path.join(_SRC_DIR, "config.json")

# =============================================================================
# STATE / ESTADO
# =============================================================================

_current_lang = "en"
_translations = {}
_available_languages = {}
_change_callbacks = []  # Callbacks for hot-reload / Callbacks para recarga en caliente

# =============================================================================
# LANGUAGE LOADING / CARGA DE IDIOMAS
# =============================================================================

def _load_language(lang_code):
    """Load a language file / Carga un archivo de idioma"""
    filepath = os.path.join(LANG_DIR, f"{lang_code}.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None


def _load_available_languages():
    """Scan lang/ folder for available languages / Escanea carpeta lang/ buscando idiomas"""
    global _available_languages
    _available_languages = {}
    
    if not os.path.exists(LANG_DIR):
        return
    
    for filename in os.listdir(LANG_DIR):
        if filename.endswith('.json'):
            lang_code = filename[:-5]  # Remove .json
            data = _load_language(lang_code)
            if data and "_meta" in data:
                _available_languages[lang_code] = {
                    "code": lang_code,
                    "name_native": data["_meta"].get("name_native", lang_code),
                    "name_english": data["_meta"].get("name_english", lang_code),
                    "flag": data["_meta"].get("flag", "🏳️")
                }


def get_available_languages():
    """
    Get dict of available languages
    Obtiene dict de idiomas disponibles
    
    Returns:
        dict: {code: {code, name_native, name_english}, ...}
    """
    if not _available_languages:
        _load_available_languages()
    return _available_languages


def get_language_display_list():
    """
    Get list for language selector: "Native / English"
    Obtiene lista para selector: "Nativo / English"
    
    Returns:
        list: [(code, "Español / Spanish"), ...]
    """
    langs = get_available_languages()
    result = []
    for code, info in sorted(langs.items(), key=lambda x: x[1]["name_english"]):
        display = f"{info['name_native']} / {info['name_english']}"
        result.append((code, display))
    return result


def get_current_flag():
    """
    Get flag emoji for current language
    Obtiene emoji de bandera del idioma actual
    
    Returns:
        str: Flag emoji (e.g. "🇪🇸")
    """
    langs = get_available_languages()
    if _current_lang in langs:
        return langs[_current_lang].get("flag", "🏳️")
    return "🏳️"


def get_language_flag_list():
    """
    Get list for language dropdown with flags
    Obtiene lista para dropdown con banderas
    
    Returns:
        list: [(code, flag, "Native / English"), ...]
    """
    langs = get_available_languages()
    result = []
    for code, info in sorted(langs.items(), key=lambda x: x[1]["name_english"]):
        flag = info.get("flag", "🏳️")
        display = f"{info['name_native']} / {info['name_english']}"
        result.append((code, flag, display))
    return result


# =============================================================================
# LANGUAGE SELECTION / SELECCIÓN DE IDIOMA
# =============================================================================

def _detect_system_language():
    """Detect system language / Detecta idioma del sistema"""
    try:
        system_locale = locale.getdefaultlocale()[0]  # e.g. 'es_ES', 'en_US'
        if system_locale:
            lang_code = system_locale.split('_')[0]  # e.g. 'es', 'en'
            if lang_code in get_available_languages():
                return lang_code
    except:
        pass
    return "en"


def _load_config():
    """Load config file / Carga archivo de configuración"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def _save_config(config):
    """Save config file / Guarda archivo de configuración"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except:
        pass


def init(default_lang=None):
    """
    Initialize i18n system
    Inicializa sistema i18n
    
    Args:
        default_lang: Force specific language, or None for auto-detect
    """
    global _current_lang, _translations
    
    _load_available_languages()
    
    # Priority: config > default_lang > system > english
    config = _load_config()
    lang = config.get("language")
    
    if not lang or lang not in _available_languages:
        lang = default_lang
    
    if not lang or lang not in _available_languages:
        lang = _detect_system_language()
    
    if not lang or lang not in _available_languages:
        lang = "en"
    
    _current_lang = lang
    _translations = _load_language(lang) or {}


def get_current_language():
    """Get current language code / Obtiene código de idioma actual"""
    return _current_lang


def set_language(lang_code):
    """
    Change language and notify callbacks (hot-reload)
    Cambia idioma y notifica callbacks (recarga en caliente)
    
    Args:
        lang_code: Language code (en, es, fr, etc.)
    
    Returns:
        bool: True if changed successfully
    """
    global _current_lang, _translations
    
    if lang_code not in get_available_languages():
        return False
    
    _current_lang = lang_code
    _translations = _load_language(lang_code) or {}
    
    # Save preference / Guardar preferencia
    config = _load_config()
    config["language"] = lang_code
    _save_config(config)
    
    # Notify callbacks / Notificar callbacks
    for callback in _change_callbacks:
        try:
            callback()
        except:
            pass
    
    return True


def on_language_change(callback):
    """
    Register callback for language changes (hot-reload)
    Registra callback para cambios de idioma (recarga en caliente)
    
    Args:
        callback: Function to call when language changes
    """
    if callback not in _change_callbacks:
        _change_callbacks.append(callback)


def remove_language_callback(callback):
    """Remove a registered callback / Elimina un callback registrado"""
    if callback in _change_callbacks:
        _change_callbacks.remove(callback)


# =============================================================================
# TRANSLATION / TRADUCCIÓN
# =============================================================================

def t(key, **kwargs):
    """
    Get translated string by key
    Obtiene cadena traducida por clave
    
    Args:
        key: Dot-notation key (e.g. "menu.file")
        **kwargs: Format arguments (e.g. filename="doc.md")
    
    Returns:
        str: Translated string, or key if not found
    
    Example:
        t("menu.file") -> "Archivo"
        t("status.saved", filename="doc.md") -> "Guardado: doc.md"
    """
    # Navigate nested dict with dot notation
    parts = key.split(".")
    value = _translations
    
    for part in parts:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return key  # Key not found, return as-is
    
    if not isinstance(value, str):
        return key
    
    # Format with kwargs if provided
    if kwargs:
        try:
            return value.format(**kwargs)
        except:
            return value
    
    return value


# Alias for convenience / Alias por conveniencia
get_text = t
