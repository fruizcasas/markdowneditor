// ========== STORAGE ==========

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
            if (s.style) {
                currentStyle = s.style;
                document.getElementById('styleSelect').value = s.style;
            }
            if (s.lang) {
                currentLang = s.lang;
                document.getElementById('langSelect').value = s.lang;
            }
            if (s.theme === 'light') {
                document.body.classList.add('light-theme');
                document.getElementById('themeBtn').textContent = '☀️';
            }
        } catch(e) {}
    }

    if (saved && saved.trim()) {
        editor.value = saved;
        showToast(t('status.restored'));
        return true;
    }
    return false;
}
