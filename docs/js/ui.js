// ========== UI UTILITIES ==========

function showToast(msg, isUpdate = false) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = 'toast show' + (isUpdate ? ' update' : '');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

// Store scroll position between panels
let lastScrollPercent = 0;

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
