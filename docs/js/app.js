// ========== MAIN APP ==========
// Entry point - initializes all modules

function init() {
    initEditor();
    registerSW();
}

// Start app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
