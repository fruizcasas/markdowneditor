// ========== UI UTILITIES ==========

function showToast(msg, isUpdate = false) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = 'toast show' + (isUpdate ? ' update' : '');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

function showPanel(panel) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(panel + 'Panel').classList.add('active');
    if (panel === 'preview') updatePreview();
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
