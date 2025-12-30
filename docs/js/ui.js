// ========== UI UTILITIES ==========

function showToast(msg, isUpdate = false) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = 'toast show' + (isUpdate ? ' update' : '');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

// Store scroll position between panels
let lastScrollPercent = 0;
let isScrollSyncing = false; // Prevent infinite scroll loops
let scrollSyncEnabled = true; // Toggle for scroll sync

// ========== ZOOM ==========

const ZOOM_MIN = 10;
const ZOOM_MAX = 32;
const ZOOM_STEP = 2;
const ZOOM_DEFAULT_EDITOR = 16;
const ZOOM_DEFAULT_PREVIEW = 16;

let editorZoom = ZOOM_DEFAULT_EDITOR;
let previewZoom = ZOOM_DEFAULT_PREVIEW;

function initZoom() {
    // Load saved zoom levels
    const settings = JSON.parse(localStorage.getItem(STORAGE_SETTINGS) || '{}');
    editorZoom = settings.editorZoom || ZOOM_DEFAULT_EDITOR;
    previewZoom = settings.previewZoom || ZOOM_DEFAULT_PREVIEW;

    applyEditorZoom();
    updateZoomLabels();
}

function saveZoomSettings() {
    const settings = JSON.parse(localStorage.getItem(STORAGE_SETTINGS) || '{}');
    settings.editorZoom = editorZoom;
    settings.previewZoom = previewZoom;
    localStorage.setItem(STORAGE_SETTINGS, JSON.stringify(settings));
}

function updateZoomLabels() {
    document.getElementById('editorZoomLabel').textContent = editorZoom + 'px';
    document.getElementById('previewZoomLabel').textContent = previewZoom + 'px';
}

function applyEditorZoom() {
    document.getElementById('editor').style.fontSize = editorZoom + 'px';
}

function editorZoomIn() {
    if (editorZoom < ZOOM_MAX) {
        editorZoom += ZOOM_STEP;
        applyEditorZoom();
        updateZoomLabels();
        saveZoomSettings();
    }
}

function editorZoomOut() {
    if (editorZoom > ZOOM_MIN) {
        editorZoom -= ZOOM_STEP;
        applyEditorZoom();
        updateZoomLabels();
        saveZoomSettings();
    }
}

function previewZoomIn() {
    if (previewZoom < ZOOM_MAX) {
        previewZoom += ZOOM_STEP;
        updateZoomLabels();
        saveZoomSettings();
        updatePreview();
    }
}

function previewZoomOut() {
    if (previewZoom > ZOOM_MIN) {
        previewZoom -= ZOOM_STEP;
        updateZoomLabels();
        saveZoomSettings();
        updatePreview();
    }
}

function getPreviewZoomCSS() {
    return `
        body { font-size: ${previewZoom}px !important; }
        p, li, td, th, dd, dt { font-size: inherit !important; }
        h1 { font-size: 2em !important; }
        h2 { font-size: 1.5em !important; }
        h3 { font-size: 1.25em !important; }
        pre, code { font-size: 0.9em !important; }
    `;
}

// ========== REAL-TIME SCROLL SYNC ==========

function initScrollSync() {
    const editor = document.getElementById('editor');
    const preview = document.getElementById('preview');

    // Sync editor scroll to preview
    editor.addEventListener('scroll', () => {
        if (!scrollSyncEnabled) return;
        if (isScrollSyncing) return;
        if (window.innerWidth <= 768) return; // Only sync in dual-pane mode

        const maxScroll = editor.scrollHeight - editor.clientHeight;
        if (maxScroll <= 0) return;

        const percent = editor.scrollTop / maxScroll;
        syncPreviewScroll(percent);
    });

    // Sync preview scroll to editor (when preview iframe loads)
    preview.addEventListener('load', () => {
        try {
            const doc = preview.contentDocument;
            if (!doc) return;

            doc.addEventListener('scroll', () => {
                if (!scrollSyncEnabled) return;
                if (isScrollSyncing) return;
                if (window.innerWidth <= 768) return;

                const html = doc.documentElement;
                const maxScroll = html.scrollHeight - html.clientHeight;
                if (maxScroll <= 0) return;

                const percent = html.scrollTop / maxScroll;
                syncEditorScroll(percent);
            });
        } catch (e) {}
    });
}

function toggleScrollSync() {
    const checkbox = document.getElementById('scrollSyncCheckbox');
    scrollSyncEnabled = checkbox.checked;
}

function manualScrollSync() {
    // Sync preview to current editor position
    const editor = document.getElementById('editor');
    const maxScroll = editor.scrollHeight - editor.clientHeight;
    if (maxScroll <= 0) return;

    const percent = editor.scrollTop / maxScroll;
    syncPreviewScroll(percent);
    showToast(scrollSyncEnabled ? '🔗 Sincronizado' : '🔗 Sincronizado (auto desactivado)');
}

function syncPreviewScroll(percent) {
    const preview = document.getElementById('preview');
    try {
        const doc = preview.contentDocument;
        if (!doc) return;

        const html = doc.documentElement;
        const maxScroll = html.scrollHeight - html.clientHeight;

        isScrollSyncing = true;
        html.scrollTop = maxScroll * percent;
        setTimeout(() => { isScrollSyncing = false; }, 50);
    } catch (e) {}
}

function syncEditorScroll(percent) {
    const editor = document.getElementById('editor');
    const maxScroll = editor.scrollHeight - editor.clientHeight;

    isScrollSyncing = true;
    editor.scrollTop = maxScroll * percent;
    setTimeout(() => { isScrollSyncing = false; }, 50);
}

function showPanel(panel) {
    // Get current scroll percentage before switching
    const editorEl = document.getElementById('editor');
    const previewEl = document.getElementById('preview');

    const editorPanel = document.getElementById('editorPanel');
    const previewPanel = document.getElementById('previewPanel');

    // Save scroll position from current active panel
    if (editorPanel.classList.contains('active') && editorEl) {
        const maxScroll = editorEl.scrollHeight - editorEl.clientHeight;
        lastScrollPercent = maxScroll > 0 ? editorEl.scrollTop / maxScroll : 0;
    } else if (previewPanel.classList.contains('active') && previewEl.contentDocument) {
        try {
            const doc = previewEl.contentDocument.documentElement;
            const maxScroll = doc.scrollHeight - doc.clientHeight;
            lastScrollPercent = maxScroll > 0 ? doc.scrollTop / maxScroll : 0;
        } catch (e) {}
    }

    // Switch panels
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(panel + 'Panel').classList.add('active');

    // Apply scroll position to new panel
    if (panel === 'preview') {
        updatePreview();
        // Wait for preview to render, then scroll
        setTimeout(() => {
            if (previewEl.contentDocument) {
                try {
                    const doc = previewEl.contentDocument.documentElement;
                    const maxScroll = doc.scrollHeight - doc.clientHeight;
                    doc.scrollTop = maxScroll * lastScrollPercent;
                } catch (e) {}
            }
        }, 100);
    } else if (panel === 'editor' && editorEl) {
        const maxScroll = editorEl.scrollHeight - editorEl.clientHeight;
        editorEl.scrollTop = maxScroll * lastScrollPercent;
        editorEl.focus();
    }
}

function toggleTheme() {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    document.getElementById('themeBtn').textContent = isLight ? '☀️' : '🌙';
    autoSave();
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

// ========== MENU ==========

function toggleMenu() {
    const menu = document.getElementById('mainMenu');
    const wasOpen = menu.classList.contains('show');
    closeAllDropdowns();
    if (!wasOpen) {
        menu.classList.add('show');
    }
}

function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-content').forEach(d => d.classList.remove('show'));
}

// Global click handler to close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    // Check if click is inside a dropdown, its toggle button, or keyboard bar
    const dropdown = e.target.closest('.dropdown');
    const keyboardBar = e.target.closest('.keyboard-bar');
    if (!dropdown && !keyboardBar) {
        // Click outside any dropdown - close all
        closeAllDropdowns();
    }
});

// Also close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeAllDropdowns();
    }
});

// ========== ABOUT MODAL ==========

function showAbout() {
    closeAllDropdowns();
    document.getElementById('aboutVersion').textContent = `Markdown Editor v${APP_VERSION}`;
    document.getElementById('aboutModal').classList.add('show');
}

function closeAbout() {
    document.getElementById('aboutModal').classList.remove('show');
}

// ========== KEYBOARD ACCESSORY BAR ==========

function updateKeyboardBarPosition() {
    const bar = document.getElementById('keyboardBar');
    if (!bar.classList.contains('show')) return;

    if (window.visualViewport) {
        // Position bar at bottom of visual viewport (just above keyboard)
        const vp = window.visualViewport;
        const barHeight = bar.offsetHeight || 44;

        // In PWA standalone mode, use simpler calculation
        const isPWA = window.matchMedia('(display-mode: standalone)').matches ||
                      window.navigator.standalone === true;

        if (isPWA) {
            // PWA: position from bottom using viewport height difference
            const keyboardHeight = window.innerHeight - vp.height;
            bar.style.bottom = Math.max(0, keyboardHeight) + 'px';
            bar.style.top = 'auto';
        } else {
            // Browser: use top positioning
            bar.style.top = (vp.offsetTop + vp.height - barHeight) + 'px';
            bar.style.bottom = 'auto';
        }
    }
}

function showKeyboardBar() {
    // Only show on mobile
    if (window.innerWidth <= 768) {
        const bar = document.getElementById('keyboardBar');
        bar.classList.add('show');
        // Small delay to let keyboard fully appear
        setTimeout(updateKeyboardBarPosition, 100);
        setTimeout(updateKeyboardBarPosition, 300);
    }
}

function hideKeyboardBar() {
    const bar = document.getElementById('keyboardBar');
    bar.classList.remove('show');
    bar.style.top = 'auto';
    bar.style.bottom = '0';
}

function hideKeyboard() {
    document.getElementById('editor').blur();
    hideKeyboardBar();
}

function showKeyboardSnippets() {
    // Show snippets menu as a modal on mobile when keyboard is active
    toggleSnippets();
}

function showKeyboardStyles() {
    // Show style editor
    showStyleEditor();
}

// Setup keyboard bar events
function initKeyboardBar() {
    const editor = document.getElementById('editor');

    editor.addEventListener('focus', () => {
        showKeyboardBar();
    });

    editor.addEventListener('blur', () => {
        // Small delay to allow button clicks to register
        setTimeout(() => {
            if (document.activeElement !== editor) {
                hideKeyboardBar();
            }
        }, 150);
    });

    // Update position when visualViewport changes (keyboard opens/closes)
    if (window.visualViewport) {
        window.visualViewport.addEventListener('resize', updateKeyboardBarPosition);
        window.visualViewport.addEventListener('scroll', updateKeyboardBarPosition);
    }
}

// ========== PANEL COLLAPSE/EXPAND ==========

let editorExpanded = true;
let previewExpanded = true;
let lastWidth = window.innerWidth;

function togglePanel(panel) {
    const editorPanel = document.getElementById('editorPanel');
    const previewPanel = document.getElementById('previewPanel');
    const divider = document.getElementById('divider');
    const editorBtn = editorPanel.querySelector('.panel-collapse-btn');
    const previewBtn = previewPanel.querySelector('.panel-collapse-btn');

    if (panel === 'editor') {
        // Toggle editor visibility
        if (editorExpanded) {
            editorPanel.classList.add('hidden');
            divider.classList.add('hidden');
            editorExpanded = false;
            previewBtn.textContent = '▶';
            // Preview takes full width
            previewPanel.style.flex = '1';
        } else {
            editorPanel.classList.remove('hidden');
            divider.classList.remove('hidden');
            editorExpanded = true;
            previewBtn.textContent = '◀';
            // Reset both to 50/50
            editorPanel.style.flex = '1';
            previewPanel.style.flex = '1';
        }
    } else {
        // Toggle preview visibility
        if (previewExpanded) {
            previewPanel.classList.add('hidden');
            divider.classList.add('hidden');
            previewExpanded = false;
            editorBtn.textContent = '◀';
            // Editor takes full width
            editorPanel.style.flex = '1';
        } else {
            previewPanel.classList.remove('hidden');
            divider.classList.remove('hidden');
            previewExpanded = true;
            editorBtn.textContent = '▶';
            // Reset both to 50/50
            editorPanel.style.flex = '1';
            previewPanel.style.flex = '1';
            updatePreview();
        }
    }
}

// Reset panel states when switching between mobile/desktop modes
function resetPanelStates() {
    const editorPanel = document.getElementById('editorPanel');
    const previewPanel = document.getElementById('previewPanel');
    const divider = document.getElementById('divider');
    const editorBtn = editorPanel.querySelector('.panel-collapse-btn');
    const previewBtn = previewPanel.querySelector('.panel-collapse-btn');

    // Remove hidden class from both panels
    editorPanel.classList.remove('hidden');
    previewPanel.classList.remove('hidden');
    divider.classList.remove('hidden');

    // Reset flex styles
    editorPanel.style.flex = '';
    previewPanel.style.flex = '';

    // Reset state
    editorExpanded = true;
    previewExpanded = true;

    // Reset button icons
    if (editorBtn) editorBtn.textContent = '▶';
    if (previewBtn) previewBtn.textContent = '◀';

    // In mobile mode, show only editor tab by default
    if (window.innerWidth <= 768) {
        editorPanel.classList.add('active');
        previewPanel.classList.remove('active');
        // Update tabs
        document.querySelectorAll('.tab').forEach((tab, i) => {
            tab.classList.toggle('active', i === 0);
        });
    } else {
        // Desktop: both panels active
        editorPanel.classList.add('active');
        previewPanel.classList.add('active');
    }

    updatePreview();
}

// Listen for resize to handle orientation changes
window.addEventListener('resize', () => {
    const currentWidth = window.innerWidth;
    const crossedThreshold = (lastWidth <= 768 && currentWidth > 768) ||
                             (lastWidth > 768 && currentWidth <= 768);

    if (crossedThreshold) {
        resetPanelStates();
    }

    lastWidth = currentWidth;
});

// ========== DIVIDER DRAG ==========

function initDivider() {
    const divider = document.getElementById('divider');
    const main = document.querySelector('.main');
    const editorPanel = document.getElementById('editorPanel');
    const previewPanel = document.getElementById('previewPanel');

    let isDragging = false;

    divider.addEventListener('mousedown', startDrag);
    divider.addEventListener('touchstart', startDrag, { passive: false });

    function startDrag(e) {
        if (window.innerWidth <= 768) return; // No drag on mobile
        isDragging = true;
        divider.classList.add('dragging');
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';

        document.addEventListener('mousemove', drag);
        document.addEventListener('touchmove', drag, { passive: false });
        document.addEventListener('mouseup', stopDrag);
        document.addEventListener('touchend', stopDrag);

        e.preventDefault();
    }

    function drag(e) {
        if (!isDragging) return;

        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const mainRect = main.getBoundingClientRect();
        const percent = ((clientX - mainRect.left) / mainRect.width) * 100;

        // Limit between 20% and 80%
        const clampedPercent = Math.max(20, Math.min(80, percent));

        editorPanel.style.flex = `0 0 ${clampedPercent}%`;
        previewPanel.style.flex = `0 0 ${100 - clampedPercent}%`;
    }

    function stopDrag() {
        isDragging = false;
        divider.classList.remove('dragging');
        document.body.style.cursor = '';
        document.body.style.userSelect = '';

        document.removeEventListener('mousemove', drag);
        document.removeEventListener('touchmove', drag);
        document.removeEventListener('mouseup', stopDrag);
        document.removeEventListener('touchend', stopDrag);
    }
}
