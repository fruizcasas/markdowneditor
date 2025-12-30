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
        "update.done": "Actualizado a la ultima version"
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
        "update.done": "Updated to latest version"
    }
};

let currentLang = localStorage.getItem('md_lang') || 'es';

function t(key) {
    return i18n[currentLang][key] || key;
}

function updateTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        el.textContent = t(el.dataset.i18n);
    });
    if (typeof updateCharCount === 'function') {
        updateCharCount();
    }
}

function changeLang() {
    currentLang = document.getElementById('langSelect').value;
    localStorage.setItem('md_lang', currentLang);
    updateTexts();
}
