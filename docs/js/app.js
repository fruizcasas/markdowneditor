// ========== APP VERSION ==========
const APP_VERSION = '1.1.0';

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
        "confirm.new": "¿Crear nuevo documento?",
        "update.available": "Nueva versión disponible. Toca para actualizar.",
        "update.done": "Actualizado a la última versión"
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

function t(key) { return i18n[currentLang][key] || key; }

function updateTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        el.textContent = t(el.dataset.i18n);
    });
    updateCharCount();
}

function changeLang() {
    currentLang = document.getElementById('langSelect').value;
    localStorage.setItem('md_lang', currentLang);
    updateTexts();
}

// ========== STYLES ==========
const styles = {
    gitlab: `
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 16px; line-height: 1.6; color: #303030; background: #fff; padding: 20px; max-width: 900px; margin: 0 auto; }
        h1 { font-size: 2em; font-weight: 600; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #1f1f1f; }
        h2 { font-size: 1.5em; font-weight: 600; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #1f1f1f; }
        h3 { font-size: 1.25em; font-weight: 600; margin: 1.5em 0 0.5em; color: #1f1f1f; }
        p { margin: 0 0 1em; }
        a { color: #1068bf; text-decoration: none; }
        code { font-family: 'SF Mono', Consolas, monospace; font-size: 0.9em; background: #f5f5f5; padding: 0.2em 0.4em; border-radius: 4px; color: #d14; }
        pre { font-family: 'SF Mono', Consolas, monospace; font-size: 0.9em; background: #f6f8fa; border: 1px solid #e5e5e5; border-radius: 6px; padding: 16px; overflow-x: auto; }
        pre code { background: transparent; padding: 0; color: #303030; }
        blockquote { margin: 1em 0; padding: 0.5em 1em; border-left: 4px solid #dbdbdb; background: #fafafa; color: #666; }
        ul, ol { margin: 0 0 1em; padding-left: 2em; }
        li { margin-bottom: 0.25em; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th { background: #f6f8fa; border: 1px solid #e5e5e5; padding: 10px 12px; text-align: left; font-weight: 600; }
        td { border: 1px solid #e5e5e5; padding: 10px 12px; }
        tr:nth-child(even) { background: #fafafa; }
        hr { border: none; border-top: 1px solid #e5e5e5; margin: 2em 0; }
        img { max-width: 100%; height: auto; }
        .callout-note { background: #e7f3ff; border-left: 4px solid #0066cc; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-warning { background: #fff8e6; border-left: 4px solid #f0ad4e; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-important { background: #ffeaea; border-left: 4px solid #dc3545; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
    `,
    default: `
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; background: #fff; margin: 20px; }
        h1 { font-size: 28px; font-weight: 600; color: #1a1a1a; margin: 24px 0 16px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }
        h2 { font-size: 22px; font-weight: 600; color: #2a2a2a; margin: 20px 0 12px; border-bottom: 1px solid #e8e8e8; padding-bottom: 6px; }
        h3 { font-size: 18px; font-weight: 600; color: #3a3a3a; margin: 16px 0 10px; }
        p { margin: 0 0 12px; }
        a { color: #0066cc; text-decoration: underline; }
        code { font-family: Consolas, Monaco, monospace; font-size: 13px; color: #c7254e; background: #f9f2f4; padding: 2px 6px; border-radius: 3px; }
        pre { font-family: Consolas, Monaco, monospace; font-size: 13px; color: #333; background: #f5f5f5; padding: 16px; border-radius: 6px; border: 1px solid #e0e0e0; overflow-x: auto; }
        blockquote { font-style: italic; color: #555; background: #f8f9fa; border-left: 4px solid #6c757d; margin: 16px 0; padding: 12px 20px; }
        ul, ol { margin: 8px 0 12px; padding-left: 24px; }
        li { margin-bottom: 4px; }
        table { border-collapse: collapse; width: 100%; margin: 12px 0 16px; }
        th { font-weight: 600; color: #fff; background: #4a5568; border: 1px solid #cbd5e0; padding: 10px 12px; text-align: left; }
        td { border: 1px solid #e2e8f0; padding: 8px 12px; }
        hr { border: none; border-top: 1px solid #e0e0e0; margin: 24px 0; }
        img { max-width: 100%; height: auto; }
        .callout-note { background: #e7f3ff; border-left: 4px solid #0066cc; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-warning { background: #fff8e6; border-left: 4px solid #f0ad4e; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
        .callout-important { background: #ffeaea; border-left: 4px solid #dc3545; padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
    `
};
let currentStyle = localStorage.getItem('md_style') || 'gitlab';

// ========== STORAGE ==========
const STORAGE_KEY = 'md_editor_content';
const STORAGE_SETTINGS = 'md_editor_settings';

function autoSave() {
    localStorage.setItem(STORAGE_KEY, editor.value);
    localStorage.setItem(STORAGE_SETTINGS, JSON.stringify({
        style: currentStyle,
        lang: currentLang,
        theme: document.body.classList.contains('light-theme') ? 'light' : 'dark'
    }));
    document.getElementById('savedIndicator').textContent = '✓ ' + t('status.autosaved');
    setTimeout(() => {
        document.getElementById('savedIndicator').textContent = '';
    }, 2000);
}

function loadSaved() {
    const saved = localStorage.getItem(STORAGE_KEY);
    const settings = localStorage.getItem(STORAGE_SETTINGS);

    if (settings) {
        try {
            const s = JSON.parse(settings);
            if (s.style) { currentStyle = s.style; document.getElementById('styleSelect').value = s.style; }
            if (s.lang) { currentLang = s.lang; document.getElementById('langSelect').value = s.lang; }
            if (s.theme === 'light') { document.body.classList.add('light-theme'); document.getElementById('themeBtn').textContent = '☀️'; }
        } catch(e) {}
    }

    if (saved && saved.trim()) {
        editor.value = saved;
        showToast(t('status.restored'));
        return true;
    }
    return false;
}

// ========== EDITOR ==========
let editor, preview;
let updateTimeout, saveTimeout;

const exampleDoc = `# Bienvenido a Markdown Editor

Este editor funciona **100% offline** y guarda automáticamente tu trabajo.

## Características

- ✅ Funciona sin conexión (PWA)
- ✅ Autoguardado automático
- ✅ Actualización automática
- ✅ Optimizado para iOS

## Prueba el editor

Escribe aquí y verás la vista previa en tiempo real.

### Lista de tareas
- [ ] Escribir documento
- [ ] Revisar formato
- [ ] Compartir resultado

> **Tip:** En móvil, usa las pestañas para cambiar entre editor y vista previa.

---
*Markdown Editor PWA v${APP_VERSION}*
`;

function init() {
    editor = document.getElementById('editor');
    preview = document.getElementById('preview');

    // Load saved content or example
    if (!loadSaved()) {
        editor.value = exampleDoc;
    }

    updatePreview();
    updateCharCount();
    updateTexts();

    // Auto-save on input
    editor.addEventListener('input', () => {
        clearTimeout(updateTimeout);
        clearTimeout(saveTimeout);
        updateTimeout = setTimeout(updatePreview, 300);
        saveTimeout = setTimeout(autoSave, 1000);
        updateCharCount();
    });

    // Divider drag (desktop)
    const divider = document.getElementById('divider');
    let isDragging = false;
    divider.addEventListener('mousedown', () => isDragging = true);
    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const container = document.querySelector('.main');
        const rect = container.getBoundingClientRect();
        const percent = ((e.clientX - rect.left) / rect.width) * 100;
        document.getElementById('editorPanel').style.flex = `0 0 ${percent}%`;
        document.getElementById('previewPanel').style.flex = `0 0 ${100 - percent}%`;
    });
    document.addEventListener('mouseup', () => isDragging = false);

    // File input
    document.getElementById('fileInput').addEventListener('change', handleFileOpen);

    // Show both panels on desktop
    if (window.innerWidth > 768) {
        document.getElementById('previewPanel').classList.add('active');
    }

    // Register Service Worker
    registerSW();
}

function updatePreview() {
    const html = marked.parse(editor.value);
    const fullHtml = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>${styles[currentStyle]}</style></head><body>${html}</body></html>`;
    preview.srcdoc = fullHtml;
}

function updateCharCount() {
    document.getElementById('charCount').textContent = `${editor.value.length} ${t('chars')}`;
}

function changeStyle() {
    currentStyle = document.getElementById('styleSelect').value;
    localStorage.setItem('md_style', currentStyle);
    updatePreview();
}

// ========== ACTIONS ==========
function newDoc() {
    if (confirm(t('confirm.new'))) {
        editor.value = '';
        updatePreview();
        updateCharCount();
        autoSave();
        showToast(t('status.new'));
    }
}

function openFile() {
    document.getElementById('fileInput').click();
}

function handleFileOpen(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
        editor.value = event.target.result;
        updatePreview();
        updateCharCount();
        autoSave();
        showToast(t('status.opened') + ': ' + file.name);
    };
    reader.readAsText(file);
    e.target.value = '';
}

function saveFile() {
    const blob = new Blob([editor.value], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'documento.md';
    a.click();
    URL.revokeObjectURL(url);
    showToast(t('status.saved'));
}

function shareContent() {
    if (navigator.share) {
        navigator.share({
            title: 'Markdown Document',
            text: editor.value
        }).catch(() => {});
    } else {
        copyToClipboard(editor.value);
        showToast('Texto copiado');
    }
}

function copyHtml() {
    const html = marked.parse(editor.value);
    const fullHtml = `<!DOCTYPE html><html><head><meta charset="UTF-8"><style>${styles[currentStyle]}</style></head><body>${html}</body></html>`;
    copyToClipboard(fullHtml);
    showToast(t('status.copied'));
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
}

function toggleTheme() {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    document.getElementById('themeBtn').textContent = isLight ? '☀️' : '🌙';
    autoSave();
}

function showPanel(panel) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(panel + 'Panel').classList.add('active');
    if (panel === 'preview') updatePreview();
}

function showToast(msg, isUpdate = false) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = 'toast show' + (isUpdate ? ' update' : '');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

// ========== SERVICE WORKER & UPDATES ==========
let newWorker;

function registerSW() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').then(reg => {
            // Check for updates
            reg.addEventListener('updatefound', () => {
                newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // New version available
                        document.getElementById('updateBanner').classList.add('show');
                    }
                });
            });
        }).catch(err => console.log('SW registration failed:', err));

        // Handle controller change (reload on update)
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            window.location.reload();
        });
    }
}

function updateApp() {
    if (newWorker) {
        newWorker.postMessage('skipWaiting');
    }
    document.getElementById('updateBanner').classList.remove('show');
    showToast(t('update.done'), true);
}

// Init
document.addEventListener('DOMContentLoaded', init);
