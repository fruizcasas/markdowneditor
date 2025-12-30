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

    // Divider drag (desktop)
    initDivider();

    // File input
    document.getElementById('fileInput').addEventListener('change', handleFileOpen);

    // Show both panels on desktop
    if (window.innerWidth > 768) {
        document.getElementById('previewPanel').classList.add('active');
    }
}

function initDivider() {
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
}

function updatePreview() {
    const html = marked.parse(editor.value);
    const fullHtml = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>${styles[currentStyle]}</style></head><body>${html}</body></html>`;
    preview.srcdoc = fullHtml;
}

function updateCharCount() {
    document.getElementById('charCount').textContent = `${editor.value.length} ${t('chars')}`;
}
