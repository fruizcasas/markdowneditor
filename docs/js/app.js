// ========== MAIN APP ==========
// Entry point - initializes all modules

function init() {
    initZoom();
    initEditor();
    initKeyboardBar();
    initDivider();
    initScrollSync();
    initPinchZoom();
    initMenuLang();
    registerSW();
    handleUrlParams();
}

function handleUrlParams() {
    const params = new URLSearchParams(window.location.search);

    // Handle shortcuts
    const action = params.get('action');
    if (action === 'new') {
        setTimeout(() => {
            editor.value = generateExampleDoc();
            updatePreview();
            updateCharCount();
            autoSave();
            showToast(t('status.new'));
        }, 100);
    } else if (action === 'open') {
        setTimeout(() => openFile(), 100);
    }

    // Handle share target (text shared to app)
    const sharedText = params.get('text');
    if (sharedText) {
        setTimeout(() => {
            editor.value = sharedText;
            updatePreview();
            updateCharCount();
            autoSave();
            showToast(t('status.opened'));
        }, 100);
    }

    // Clean URL
    if (params.toString()) {
        window.history.replaceState({}, '', window.location.pathname);
    }
}

// Start app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
