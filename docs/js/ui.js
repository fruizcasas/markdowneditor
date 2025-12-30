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
    closeAllDropdowns();
    menu.classList.toggle('show');

    if (menu.classList.contains('show')) {
        setTimeout(() => {
            document.addEventListener('click', closeMenuOnClickOutside);
        }, 10);
    }
}

function closeMenuOnClickOutside(e) {
    const menu = document.getElementById('mainMenu');
    const btn = e.target.closest('.dropdown');
    if (!btn || !btn.contains(menu)) {
        menu.classList.remove('show');
        document.removeEventListener('click', closeMenuOnClickOutside);
    }
}

function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-content').forEach(d => d.classList.remove('show'));
}

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
        // Calculate keyboard height using visualViewport
        const keyboardHeight = window.innerHeight - window.visualViewport.height;
        bar.style.bottom = keyboardHeight + 'px';
    }
}

function showKeyboardBar() {
    // Only show on mobile
    if (window.innerWidth <= 768) {
        const bar = document.getElementById('keyboardBar');
        bar.classList.add('show');
        updateKeyboardBarPosition();
    }
}

function hideKeyboardBar() {
    const bar = document.getElementById('keyboardBar');
    bar.classList.remove('show');
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

function togglePanel(panel) {
    const editorPanel = document.getElementById('editorPanel');
    const previewPanel = document.getElementById('previewPanel');
    const editorBtn = editorPanel.querySelector('.panel-collapse-btn');
    const previewBtn = previewPanel.querySelector('.panel-collapse-btn');

    if (panel === 'editor') {
        // Toggle editor visibility
        if (editorExpanded) {
            editorPanel.classList.add('hidden');
            editorExpanded = false;
            previewBtn.textContent = '▶'; // Click to show editor
        } else {
            editorPanel.classList.remove('hidden');
            editorExpanded = true;
            previewBtn.textContent = '◀'; // Click to hide editor
        }
    } else {
        // Toggle preview visibility
        if (previewExpanded) {
            previewPanel.classList.add('hidden');
            previewExpanded = false;
            editorBtn.textContent = '◀'; // Click to show preview
        } else {
            previewPanel.classList.remove('hidden');
            previewExpanded = true;
            editorBtn.textContent = '▶'; // Click to hide preview
            updatePreview();
        }
    }
}

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
