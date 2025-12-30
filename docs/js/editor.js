// ========== EDITOR ==========
let editor, preview;
let updateTimeout, saveTimeout;

function initEditor() {
    editor = document.getElementById('editor');
    preview = document.getElementById('preview');

    // Build snippets menu
    buildSnippetsMenu();

    // Load saved content or generate example
    if (!loadSaved()) {
        editor.value = generateExampleDoc();
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

    // File inputs
    document.getElementById('fileInput').addEventListener('change', handleFileOpen);
    document.getElementById('wordInput').addEventListener('change', handleWordImport);

    // Show both panels on desktop
    if (window.innerWidth > 768) {
        document.getElementById('previewPanel').classList.add('active');
    }
}

function updatePreview() {
    const html = marked.parse(editor.value);
    const zoomCSS = typeof getPreviewZoomCSS === 'function' ? getPreviewZoomCSS() : '';
    const fullHtml = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>${styles[currentStyle]}${zoomCSS}</style></head><body>${html}</body></html>`;
    preview.srcdoc = fullHtml;
}

function updateCharCount() {
    document.getElementById('charCount').textContent = `${editor.value.length} ${t('chars')}`;
}
