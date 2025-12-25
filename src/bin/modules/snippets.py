# -*- coding: utf-8 -*-
"""
Markdown Editor - Context menu snippets and example document
Snippets del menú contextual y documento de ejemplo

Author/Autor: Fernando Ruiz Casas (fruizcasas@gmail.com)
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: December 2025 / Diciembre 2025

Copyright (c) 2025 Fernando Ruiz Casas
Licensed under MIT License
"""

from .i18n import t

# =============================================================================
# SNIPPET KEYS - Define order and separators
# CLAVES SNIPPET - Define orden y separadores
# =============================================================================

# Order of snippets with None for separators
# Orden de snippets con None para separadores
SNIPPET_ORDER = [
    "h1", "h2", "h3",
    None,  # separator
    "bullet_list", "numbered_list",
    None,  # separator
    "table", "code_block", "inline_code",
    None,  # separator
    "quote", "link", "image", "separator",
    None,  # separator
    "note", "warning", "important",
    None,  # separator
    "bold", "italic", "strikethrough",
]


def get_snippets():
    """
    Get translated snippets for context menu
    Obtiene snippets traducidos para menú contextual
    
    Returns dict with label -> content, None for separators
    Devuelve dict con label -> content, None para separadores
    """
    snippets = {}
    sep_count = 0
    
    for key in SNIPPET_ORDER:
        if key is None:
            # Unique separator key / Clave separador única
            sep_count += 1
            snippets[f"---{sep_count}"] = None
        else:
            label = t(f"snippet.{key}.label")
            content = t(f"snippet.{key}.content")
            snippets[label] = content
    
    return snippets


def get_example_document():
    """
    Generate translated example document using snippets
    Genera documento de ejemplo traducido usando snippets
    """
    # Helper to get snippet content / Helper para obtener contenido de snippet
    def s(key):
        return t(f"snippet.{key}.content")
    
    # Helper to get example text / Helper para obtener texto de ejemplo  
    def e(key):
        return t(f"example.{key}")
    
    return f"""# {e('title')}

{e('intro')}

## {e('section_text_format')}

{e('text_format_desc')}

{e('text_format_inline')}

## {e('section_lists')}

### {t('snippet.bullet_list.label')}
{s('bullet_list')}
### {t('snippet.numbered_list.label')}
{s('numbered_list')}
## {e('section_data_table')}

{s('table')}
## {e('section_code_block')}

{s('code_block')}
## {e('section_quote')}

{e('quote_text')}

## {e('section_callouts')}

{s('note')}{s('warning')}{s('important')}---

*{e('footer')}*
"""


# =============================================================================
# LEGACY FALLBACK - Used if i18n not ready
# FALLBACK LEGACY - Usado si i18n no está listo
# =============================================================================

MARKDOWN_SNIPPETS = {
    "Encabezado H1": "# Titulo principal\n\n",
    "Encabezado H2": "## Seccion\n\n",
    "Encabezado H3": "### Subseccion\n\n",
    "---": None,
    "Lista con bullets": "- Elemento 1\n- Elemento 2\n- Elemento 3\n\n",
    "Lista numerada": "1. Primer paso\n2. Segundo paso\n3. Tercer paso\n\n",
    "----": None,
    "Tabla": """| Columna 1 | Columna 2 | Columna 3 |
|-----------|-----------|-----------|
| Dato 1    | Dato 2    | Dato 3    |
| Dato 4    | Dato 5    | Dato 6    |

""",
    "Bloque de codigo": """```python
# Tu codigo aqui
def ejemplo():
    return "Hola mundo"
```

""",
    "Codigo inline": "`codigo aqui`",
    "-----": None,
    "Cita": "> Esta es una cita o nota importante.\n> Puede tener multiples lineas.\n\n",
    "Enlace": "[Texto del enlace](https://url-aqui.com)",
    "Imagen": "![Texto alternativo](ruta/a/imagen.png)",
    "Separador horizontal": "\n---\n\n",
    "------": None,
    "Nota": """<div class="callout-note">

**Nota:** Informacion adicional o aclaracion que puede ser util.

</div>

""",
    "Advertencia": """<div class="callout-warning">

**Advertencia:** Precaucion, hay algo importante que considerar aqui.

</div>

""",
    "Importante": """<div class="callout-important">

**Importante:** Atencion critica requerida. No ignorar este punto.

</div>

""",
    "-------": None,
    "Texto en negrita": "**texto en negrita**",
    "Texto en cursiva": "*texto en cursiva*",
    "Texto tachado": "~~texto tachado~~",
}

# =============================================================================
# EXAMPLE DOCUMENT / DOCUMENTO DE EJEMPLO
# =============================================================================

EXAMPLE_DOCUMENT = """# Documento de Ejemplo

Este es un documento de prueba para ver todas las capacidades del editor.

## Formato de Texto

Puedes usar **negrita**, *cursiva*, o ~~tachado~~ segun necesites.

Tambien puedes incluir `codigo inline` dentro del texto.

## Listas

### Lista con bullets
- Elemento uno
- Elemento dos
- Elemento tres

### Lista numerada
1. Primer paso
2. Segundo paso
3. Tercer paso

## Tabla de Datos

| Producto | Cantidad | Precio |
|----------|----------|--------|
| Widget A | 100      | 25.00  |
| Widget B | 50       | 45.00  |
| Widget C | 200      | 12.50  |

## Bloque de Codigo

```python
def calcular_total(items):
    return sum(item.precio * item.cantidad for item in items)
```

## Cita

> "La simplicidad es la maxima sofisticacion."
> - Leonardo da Vinci

## Callouts

<div class="callout-note">

**Nota:** Esta es una nota informativa que destaca informacion util.

</div>

<div class="callout-warning">

**Advertencia:** Cuidado con este punto, requiere atencion especial.

</div>

<div class="callout-important">

**Importante:** Esto es critico y no debe ignorarse.

</div>

---

*Documento generado con Markdown Editor*
"""
