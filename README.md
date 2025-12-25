# Markdown Editor

**Author/Autor:** Fernando Ruiz Casas (fruizcasas@gmail.com)  
**Assistant/Asistente:** Claude (Anthropic Opus 4.5)  
**Date/Fecha:** December 2025 / Diciembre 2025  
**Version/Versión:** 1.2.0  
**License/Licencia:** MIT

---

## Description / Descripción

A Markdown editor with live preview, multi-language UI, CSS styles, and PDF export.  
Un editor Markdown con vista previa en vivo, interfaz multi-idioma, estilos CSS y exportación a PDF.

---

## Features / Características

- **Live preview** with CSS styles / **Vista previa en vivo** con estilos CSS
- **Multi-language UI** (EN/ES/FR/DE/IT/PT/ZH) / **Interfaz multi-idioma**
- **Find and Replace** (Ctrl+F / Ctrl+H) / **Buscar y Reemplazar**
- **Style profiles** with visual CSS editor / **Perfiles de estilo** con editor CSS visual
- **PDF export** (requires wkhtmltopdf) / **Exportación PDF** (requiere wkhtmltopdf)
- **HTML export** for Outlook / **Exportación HTML** para Outlook
- **Drag & Drop** to open files / **Arrastrar y soltar** para abrir archivos
- **Freeze preview** for large files / **Congelar preview** para archivos grandes
- **Zoom controls** for editor and preview / **Controles de zoom** para editor y preview
- **Dark/Light theme** toggle / Alternar **tema oscuro/claro**
- **Context menu** with Markdown snippets / **Menú contextual** con snippets Markdown

---

## For Developers / Para Desarrolladores

**Want to create your own Python application without knowing Python?**  
**¿Quieres crear tu propia aplicación Python sin saber Python?**

Check out [`NEW_PY_APP.md`](NEW_PY_APP.md) - A complete guide to create any Python GUI application using Claude as your programming assistant. No Python knowledge required!

Consulta [`NEW_PY_APP.md`](NEW_PY_APP.md) - Una guía completa para crear cualquier aplicación Python con interfaz gráfica usando Claude como tu asistente de programación. ¡No se requiere conocimiento de Python!

---

## Project Structure / Estructura del proyecto

```
MarkDownEditor/
├── README.md                 # This file / Este archivo
├── NEW_PY_APP.md             # Guide to create Python apps / Guía para crear apps Python
├── publish.bat               # Generate zip in dist/ / Genera zip en dist/
├── git_init.bat              # Initialize git repo / Inicializar repo git
├── .gitignore                # Git ignore file / Archivo git ignore
│
├── src/                      # DEVELOPMENT / DESARROLLO
│   ├── 1_Install.bat         # Install dependencies / Instalar dependencias
│   ├── MarkdownEditor.bat    # Run application / Ejecutar aplicación
│   ├── README.txt            # User instructions / Instrucciones usuario
│   ├── config.json           # User preferences / Preferencias usuario
│   ├── bin/
│   │   ├── main.py           # Entry point / Punto de entrada
│   │   └── modules/          # Application modules / Módulos de la aplicación
│   ├── lang/                 # Language files / Archivos de idioma
│   │   ├── en.json, es.json, fr.json, de.json, it.json, pt.json, zh.json
│   ├── styles/               # CSS style profiles / Perfiles estilo CSS
│   └── wkhtmltopdf/          # PDF tool (download separately / descargar aparte)
│
└── dist/                     # DISTRIBUTION / DISTRIBUCIÓN (generated zips)
```

---

## Modules / Módulos

| File / Archivo | Responsibility / Responsabilidad |
|----------------|----------------------------------|
| main.py | Entry point / Punto de entrada |
| config.py | Paths, version, UI config / Rutas, versión, config UI |
| i18n.py | Internationalization / Internacionalización |
| icons.py | Emoji icons / Iconos emoji |
| snippets.py | Snippets and example document / Snippets y documento ejemplo |
| styles.py | Load/save style profiles / Carga/guarda perfiles de estilo |
| style_editor.py | Visual CSS editor window / Ventana editor CSS visual |
| renderer.py | Convert Markdown to HTML / Convierte Markdown a HTML |
| exporter.py | Export PDF and HTML / Exporta PDF y HTML |
| file_ops.py | File operations, dirty flag / Operaciones archivo, flag cambios |
| find_replace.py | Find and replace bar / Barra buscar y reemplazar |
| dnd_support.py | Drag & Drop support / Soporte arrastrar y soltar |
| zoom.py | Zoom for editor and preview / Zoom para editor y preview |
| app.py | Main class with all UI / Clase principal con toda la UI |

---

## Keyboard Shortcuts / Atajos de teclado

| Shortcut / Atajo | Action / Acción |
|------------------|-----------------|
| Ctrl+N | New document / Nuevo documento |
| Ctrl+O | Open file / Abrir archivo |
| Ctrl+S | Save / Guardar |
| Ctrl+Shift+S | Save as / Guardar como |
| Ctrl+Z | Undo / Deshacer |
| Ctrl+Y | Redo / Rehacer |
| Ctrl+X/C/V | Cut/Copy/Paste / Cortar/Copiar/Pegar |
| Ctrl+F | Find / Buscar |
| Ctrl+H | Find and Replace / Buscar y reemplazar |
| F3 | Find next / Buscar siguiente |
| Shift+F3 | Find previous / Buscar anterior |
| Ctrl+MouseWheel | Zoom editor / Zoom editor |
| Escape | Close find bar / Cerrar barra búsqueda |

---

## Requirements / Requisitos

- Python 3.10+ (Microsoft Store recommended / recomendado)
- Dependencies installed via `1_Install.bat` / Dependencias instaladas vía `1_Install.bat`
- wkhtmltopdf for PDF export (optional, download separately)  
  wkhtmltopdf para exportación PDF (opcional, descargar aparte)

---

## Quick Start / Inicio rápido

1. Run `src/1_Install.bat` to install dependencies / Ejecuta `src/1_Install.bat` para instalar dependencias
2. Run `src/MarkdownEditor.bat` to start / Ejecuta `src/MarkdownEditor.bat` para iniciar
3. For PDF export, download wkhtmltopdf to `src/wkhtmltopdf/` / Para exportar PDF, descarga wkhtmltopdf a `src/wkhtmltopdf/`

---

## License / Licencia

MIT License - See source files for details / Ver archivos fuente para detalles
