# -*- coding: utf-8 -*-
"""
Markdown Editor - Markdown to HTML conversion with CSS styles
Conversión Markdown a HTML con estilos CSS

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

import markdown


def markdown_to_html(md_text):
    """
    Convert Markdown to HTML (body only)
    Convierte Markdown a HTML (solo body)
    """
    md = markdown.Markdown(extensions=[
        'tables', 'fenced_code', 'codehilite', 'nl2br', 'sane_lists'
    ])
    return md.convert(md_text)


def style_to_css(style_data):
    """
    Convert style dict to CSS
    Convierte dict de estilo a CSS
    """
    if not style_data or "css" not in style_data:
        return ""
    
    rules = []
    for selector, props in style_data["css"].items():
        p = "\n    ".join(f"{k}: {v};" for k, v in props.items())
        rules.append(f"{selector} {{\n    {p}\n}}")
    return "\n\n".join(rules)


def render_full_html(md_text, style_data, extra_css=""):
    """
    Render Markdown to complete HTML with styles
    Renderiza Markdown a HTML completo con estilos
    
    Args:
        md_text: Markdown source text / Texto fuente Markdown
        style_data: Style dict with CSS rules / Dict de estilo con reglas CSS
        extra_css: Additional CSS (e.g. zoom) / CSS adicional (ej: zoom)
    
    Returns:
        Complete HTML document / Documento HTML completo
    """
    body = markdown_to_html(md_text)
    css = style_to_css(style_data)
    
    # Add extra CSS (e.g. zoom) / Añadir CSS extra (ej: zoom)
    if extra_css:
        css = extra_css + "\n\n" + css
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
{css}
    </style>
</head>
<body>
{body}
</body>
</html>"""
