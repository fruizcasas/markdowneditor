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

    // Drag and drop files
    initDragDrop();

    // Show both panels on desktop
    if (window.innerWidth > 768) {
        document.getElementById('previewPanel').classList.add('active');
    }
}

function initDragDrop() {
    const editorEl = document.getElementById('editor');
    const container = document.querySelector('.editor-container');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
        container.addEventListener(event, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    // Visual feedback
    ['dragenter', 'dragover'].forEach(event => {
        container.addEventListener(event, () => {
            container.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(event => {
        container.addEventListener(event, () => {
            container.classList.remove('drag-over');
        });
    });

    // Handle drop
    container.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            const validExts = ['.md', '.markdown', '.txt'];
            const ext = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));

            if (validExts.includes(ext)) {
                const reader = new FileReader();
                reader.onload = event => {
                    saveToHistory(); // Save current state for undo
                    editor.value = event.target.result;
                    updatePreview();
                    updateCharCount();
                    autoSave();
                    showToast('📂 ' + file.name);
                };
                reader.readAsText(file);
            } else {
                showToast('❌ ' + t('error.invalidfile'));
            }
        }
    });
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
