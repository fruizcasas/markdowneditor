// ========== SERVICE WORKER MANAGER ==========
let newWorker;

function registerSW() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').then(reg => {
            // Check for updates
            reg.addEventListener('updatefound', () => {
                newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // New version available
                        document.getElementById('updateBanner').classList.add('show');
                    }
                });
            });
        }).catch(err => console.log('SW registration failed:', err));

        // Handle controller change (reload on update)
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            window.location.reload();
        });
    }
}

function updateApp() {
    if (newWorker) {
        newWorker.postMessage('skipWaiting');
    }
    document.getElementById('updateBanner').classList.remove('show');
    showToast(t('update.done'), true);
}
