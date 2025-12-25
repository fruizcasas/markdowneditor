# -*- coding: utf-8 -*-
"""
Markdown Editor - Style profile management (load, save, list)
Gestión de perfiles de estilo (carga, guarda, lista)

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import os
import json
from .config import STYLES_DIR


def ensure_styles_dir():
    """
    Create styles directory if it doesn't exist
    Crea el directorio de estilos si no existe
    """
    if not os.path.exists(STYLES_DIR):
        os.makedirs(STYLES_DIR)


def load_all_styles():
    """
    Load all available style profiles.
    Carga todos los perfiles de estilo disponibles.
    
    Returns:
        dict {filename: style_data}
    """
    ensure_styles_dir()
    styles = {}
    
    for filename in os.listdir(STYLES_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(STYLES_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    style = json.load(f)
                    style['_filepath'] = filepath
                    styles[filename] = style
            except Exception as e:
                print(f"Error cargando {filename}: {e}")
    
    return styles


def load_style(filename):
    """
    Load a specific style profile
    Carga un perfil de estilo específico
    """
    filepath = os.path.join(STYLES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            style = json.load(f)
            style['_filepath'] = filepath
            return style
    return None


def save_style(style_data, filepath=None):
    """
    Save a style profile.
    Guarda un perfil de estilo.
    
    Args:
        style_data: Style dict to save / Dict de estilo a guardar
        filepath: Path to save to, or use _filepath from style_data
                  Ruta donde guardar, o usa _filepath del style_data
    """
    if filepath is None:
        filepath = style_data.get('_filepath')
    
    if filepath is None:
        raise ValueError("No se especifico filepath para guardar")
    
    # Don't save _filepath in the file / No guardar _filepath en el archivo
    save_data = {k: v for k, v in style_data.items() if k != '_filepath'}
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=4, ensure_ascii=False)


def get_default_style():
    """
    Return a basic default style
    Retorna un estilo básico por defecto
    """
    return {
        "name": "Basico",
        "css": {
            "body": {
                "font-family": "Segoe UI, Arial, sans-serif",
                "font-size": "14px",
                "line-height": "1.6",
                "color": "#333333",
                "background-color": "#ffffff"
            }
        }
    }


def get_style_names(styles_dict):
    """
    Return list of style names for combo display
    Retorna lista de nombres de estilos para mostrar en combo
    """
    return [s.get('name', k) for k, s in styles_dict.items()]
