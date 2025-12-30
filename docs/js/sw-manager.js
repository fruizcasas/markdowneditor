// ========== SERVICE WORKER MANAGER ==========
let newWorker;
let swRegistration;

function registerSW() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').then(reg => {
            swRegistration = reg;

            // Check for updates immediately on load
            reg.update();

            // Check for updates periodically (every 60 seconds)
            setInterval(() => reg.update(), 60000);

            // Handle update found
            reg.addEventListener('updatefound', () => {
                newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // New version available - show banner
                        document.getElementById('updateBanner').classList.add('show');
                    }
                });
            });

            // If there's already a waiting worker, show update banner
            if (reg.waiting) {
                newWorker = reg.waiting;
                document.getElementById('updateBanner').classList.add('show');
            }

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

// Manual update check (can be called from console or menu)
function checkForUpdates() {
    if (swRegistration) {
        swRegistration.update().then(() => {
            showToast('Buscando actualizaciones...');
        });
    }
}
