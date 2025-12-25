# -*- coding: utf-8 -*-
"""
Icon provider for toolbar - uses Unicode emoji (no dependencies)
Proveedor de iconos para la barra - usa emoji Unicode (sin dependencias)
"""

# Unicode emoji icons - work everywhere / Iconos emoji Unicode - funcionan en todos lados
# Using colored emojis that render well on Windows / Usando emojis de color que se ven bien en Windows
ICONS = {
    "new": "📄",
    "open": "📂", 
    "save": "💾",
    "cut": "✂",
    "copy": "📋",
    "paste": "📎",
    "undo": "↩️",
    "redo": "↪️",
    "pdf": "📕",
    "html": "🌐",
    "app": "📝",
    "about": "ℹ",
    "theme_dark": "🌙",
    "theme_light": "☀",
}

def init_icons(root):
    """No-op for compatibility / No-op para compatibilidad"""
    pass

def get_icon(name, size=24):
    """Return None - we use text instead / Retorna None - usamos texto en su lugar"""
    return None

def get_icon_text(name):
    """Get emoji for icon name / Obtiene emoji para nombre de icono"""
    return ICONS.get(name, "?")

def icons_available():
    """Always True for emoji / Siempre True para emoji"""
    return True
