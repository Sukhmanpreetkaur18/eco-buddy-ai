// ============================================
// EcoBuddy AI - Service Worker
// ============================================

const CACHE_VERSION = 'v1';
const CACHE_NAME = `ecobuddy-${CACHE_VERSION}`;

// Files to cache
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png',
    '/static/manifest.json'
];

// Install event - cache files
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Cache hit - return response
                if (response) {
                    return response;
                }

                // Clone the request
                const fetchRequest = event.request.clone();

                return fetch(fetchRequest).then((response) => {
                    // Check if valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    // Clone the response
                    const responseToCache = response.clone();

                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                });
            })
            .catch(() => {
                // Offline fallback
                return caches.match('/offline.html');
            })
    );
});

// Push notification event
self.addEventListener('push', (event) => {
    const data = event.data.json();
    const options = {
        body: data.body || 'New update from EcoBuddy AI!',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-72x72.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View Details',
                icon: '/static/icons/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/icons/xmark.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification(data.title || 'EcoBuddy AI', options)
    );
});

// Notification click event
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Sync event - background sync
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-data') {
        event.waitUntil(
            // Sync data with server
            fetch('/api/sync')
                .then(response => response.json())
                .then(data => {
                    console.log('Sync completed:', data);
                })
                .catch(error => {
                    console.error('Sync failed:', error);
                })
        );
    }
});

console.log('Service Worker loaded successfully!');