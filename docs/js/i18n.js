// ========== TRANSLATIONS ==========
const i18n = {
    es: {
        "panel.editor": "Editor Markdown",
        "panel.preview": "Vista previa",
        "status.ready": "Listo",
        "status.autosaved": "Autoguardado",
        "status.copied": "HTML copiado",
        "status.saved": "Archivo guardado",
        "status.opened": "Archivo abierto",
        "status.new": "Nuevo documento",
        "status.restored": "Documento restaurado",
        "chars": "caracteres",
        "confirm.new": "Crear nuevo documento?",
        "update.available": "Nueva version disponible. Toca para actualizar.",
        "update.done": "Actualizado a la ultima version",
        "snippets.title": "Insertar",
        "snippets.headers": "Encabezados",
        "snippets.format": "Formato",
        "snippets.lists": "Listas",
        "snippets.blocks": "Bloques",
        "snippets.callouts": "Callouts",
        "example.title": "Documento de Ejemplo",
        "example.intro": "Este documento muestra todas las capacidades del editor.",
        "example.section.format": "Formato de Texto",
        "example.section.lists": "Listas",
        "example.section.table": "Tabla de Datos",
        "example.section.code": "Bloque de Codigo",
        "example.section.quote": "Cita",
        "example.section.callouts": "Callouts",
        "example.footer": "Documento generado con Markdown Editor"
    },
    en: {
        "panel.editor": "Markdown Editor",
        "panel.preview": "Preview",
        "status.ready": "Ready",
        "status.autosaved": "Autosaved",
        "status.copied": "HTML copied",
        "status.saved": "File saved",
        "status.opened": "File opened",
        "status.new": "New document",
        "status.restored": "Document restored",
        "chars": "characters",
        "confirm.new": "Create new document?",
        "update.available": "New version available. Tap to update.",
        "update.done": "Updated to latest version",
        "snippets.title": "Insert",
        "snippets.headers": "Headers",
        "snippets.format": "Format",
        "snippets.lists": "Lists",
        "snippets.blocks": "Blocks",
        "snippets.callouts": "Callouts",
        "example.title": "Example Document",
        "example.intro": "This document shows all editor capabilities.",
        "example.section.format": "Text Formatting",
        "example.section.lists": "Lists",
        "example.section.table": "Data Table",
        "example.section.code": "Code Block",
        "example.section.quote": "Quote",
        "example.section.callouts": "Callouts",
        "example.footer": "Document generated with Markdown Editor"
    }
};

// Localized snippets
const snippets = {
    es: {
        h1: { label: "Encabezado H1", content: "# Titulo principal\n\n", group: "headers" },
        h2: { label: "Encabezado H2", content: "## Seccion\n\n", group: "headers" },
        h3: { label: "Encabezado H3", content: "### Subseccion\n\n", group: "headers" },
        bold: { label: "Negrita", content: "**texto en negrita**", group: "format" },
        italic: { label: "Cursiva", content: "*texto en cursiva*", group: "format" },
        strikethrough: { label: "Tachado", content: "~~texto tachado~~", group: "format" },
        inline_code: { label: "Codigo en linea", content: "`codigo aqui`", group: "format" },
        link: { label: "Enlace", content: "[Texto del enlace](https://url-aqui.com)", group: "format" },
        image: { label: "Imagen", content: "![Texto alternativo](ruta/imagen.png)", group: "format" },
        bullet_list: { label: "Lista con vinetas", content: "- Elemento 1\n- Elemento 2\n- Elemento 3\n\n", group: "lists" },
        numbered_list: { label: "Lista numerada", content: "1. Primer paso\n2. Segundo paso\n3. Tercer paso\n\n", group: "lists" },
        task_list: { label: "Lista de tareas", content: "- [ ] Tarea pendiente\n- [x] Tarea completada\n- [ ] Otra tarea\n\n", group: "lists" },
        table: { label: "Tabla", content: "| Columna 1 | Columna 2 | Columna 3 |\n|-----------|-----------|-----------|\n| Dato 1    | Dato 2    | Dato 3    |\n| Dato 4    | Dato 5    | Dato 6    |\n\n", group: "blocks" },
        code_block: { label: "Bloque de codigo", content: "```javascript\n// Tu codigo aqui\nfunction ejemplo() {\n    return \"Hola mundo\";\n}\n```\n\n", group: "blocks" },
        quote: { label: "Cita", content: "> Esta es una cita o nota importante.\n> Puede tener multiples lineas.\n\n", group: "blocks" },
        separator: { label: "Separador", content: "\n---\n\n", group: "blocks" },
        note: { label: "Nota", content: "<div class=\"callout-note\">\n\n**Nota:** Informacion adicional que puede ser util.\n\n</div>\n\n", group: "callouts" },
        warning: { label: "Advertencia", content: "<div class=\"callout-warning\">\n\n**Advertencia:** Precaucion, algo importante a considerar.\n\n</div>\n\n", group: "callouts" },
        important: { label: "Importante", content: "<div class=\"callout-important\">\n\n**Importante:** Atencion critica requerida.\n\n</div>\n\n", group: "callouts" }
    },
    en: {
        h1: { label: "Header H1", content: "# Main Title\n\n", group: "headers" },
        h2: { label: "Header H2", content: "## Section\n\n", group: "headers" },
        h3: { label: "Header H3", content: "### Subsection\n\n", group: "headers" },
        bold: { label: "Bold", content: "**bold text**", group: "format" },
        italic: { label: "Italic", content: "*italic text*", group: "format" },
        strikethrough: { label: "Strikethrough", content: "~~strikethrough text~~", group: "format" },
        inline_code: { label: "Inline code", content: "`code here`", group: "format" },
        link: { label: "Link", content: "[Link text](https://url-here.com)", group: "format" },
        image: { label: "Image", content: "![Alt text](path/to/image.png)", group: "format" },
        bullet_list: { label: "Bullet list", content: "- Item 1\n- Item 2\n- Item 3\n\n", group: "lists" },
        numbered_list: { label: "Numbered list", content: "1. First step\n2. Second step\n3. Third step\n\n", group: "lists" },
        task_list: { label: "Task list", content: "- [ ] Pending task\n- [x] Completed task\n- [ ] Another task\n\n", group: "lists" },
        table: { label: "Table", content: "| Column 1 | Column 2 | Column 3 |\n|----------|----------|----------|\n| Data 1   | Data 2   | Data 3   |\n| Data 4   | Data 5   | Data 6   |\n\n", group: "blocks" },
        code_block: { label: "Code block", content: "```javascript\n// Your code here\nfunction example() {\n    return \"Hello world\";\n}\n```\n\n", group: "blocks" },
        quote: { label: "Quote", content: "> This is a quote or important note.\n> It can have multiple lines.\n\n", group: "blocks" },
        separator: { label: "Separator", content: "\n---\n\n", group: "blocks" },
        note: { label: "Note", content: "<div class=\"callout-note\">\n\n**Note:** Additional information that may be useful.\n\n</div>\n\n", group: "callouts" },
        warning: { label: "Warning", content: "<div class=\"callout-warning\">\n\n**Warning:** Caution, something important to consider.\n\n</div>\n\n", group: "callouts" },
        important: { label: "Important", content: "<div class=\"callout-important\">\n\n**Important:** Critical attention required.\n\n</div>\n\n", group: "callouts" }
    }
};

let currentLang = localStorage.getItem('md_lang') || 'es';

function t(key) {
    return i18n[currentLang][key] || key;
}

function getSnippets() {
    return snippets[currentLang] || snippets.es;
}

function updateTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        el.textContent = t(el.dataset.i18n);
    });
    if (typeof updateCharCount === 'function') {
        updateCharCount();
    }
    if (typeof buildSnippetsMenu === 'function') {
        buildSnippetsMenu();
    }
}

function changeLang() {
    currentLang = document.getElementById('langSelect').value;
    localStorage.setItem('md_lang', currentLang);
    updateTexts();
}
