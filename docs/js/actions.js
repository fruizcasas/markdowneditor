// ========== USER ACTIONS ==========

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
