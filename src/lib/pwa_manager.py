"""
PWA Manager for EcoBuddy AI
Manages Progressive Web App features including manifest, service worker, and push notifications.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
import json
from datetime import datetime


class PWAManager:
    """
    Manages PWA features for the EcoBuddy AI app.
    """
    
    @staticmethod
    def get_manifest() -> Dict[str, Any]:
        """
        Get the PWA manifest data.
        
        Returns:
            Manifest dictionary
        """
        return {
            "name": "EcoBuddy AI",
            "short_name": "EcoBuddy",
            "description": "Your Personal AI-Powered Sustainability Assistant",
            "start_url": "/",
            "display": "standalone",
            "orientation": "portrait",
            "background_color": "#0f172a",
            "theme_color": "#0f172a",
            "icons": [
                {
                    "src": "/static/icons/icon-72x72.png",
                    "sizes": "72x72",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-96x96.png",
                    "sizes": "96x96",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-128x128.png",
                    "sizes": "128x128",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-144x144.png",
                    "sizes": "144x144",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-152x152.png",
                    "sizes": "152x152",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-384x384.png",
                    "sizes": "384x384",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icons/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "screenshots": [
                {
                    "src": "/static/screenshots/dashboard.png",
                    "sizes": "1280x720",
                    "type": "image/png"
                },
                {
                    "src": "/static/screenshots/analytics.png",
                    "sizes": "1280x720",
                    "type": "image/png"
                }
            ],
            "categories": ["lifestyle", "productivity", "utilities"],
            "lang": "en-US",
            "dir": "ltr",
            "prefer_related_applications": False,
            "related_applications": [],
            "share_target": {
                "action": "/share",
                "method": "GET",
                "params": {
                    "title": "title",
                    "text": "text",
                    "url": "url"
                }
            }
        }
    
    @staticmethod
    def get_service_worker() -> str:
        """
        Get the service worker JavaScript code.
        
        Returns:
            Service worker code string
        """
        return """
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
        """
    
    @staticmethod
    def register_service_worker() -> str:
        """
        Generate JavaScript to register service worker.
        
        Returns:
            Registration code
        """
        return """
        // Register Service Worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then((registration) => {
                        console.log('Service Worker registered with scope:', registration.scope);
                        
                        // Check for updates
                        registration.update();
                        
                        // Handle update found
                        registration.addEventListener('updatefound', () => {
                            const newWorker = registration.installing;
                            newWorker.addEventListener('statechange', () => {
                                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                    // New version available
                                    console.log('New version available!');
                                    if (confirm('A new version of EcoBuddy AI is available. Update now?')) {
                                        window.location.reload();
                                    }
                                }
                            });
                        });
                    })
                    .catch((error) => {
                        console.error('Service Worker registration failed:', error);
                    });
            });
            
            // Push notification subscription
            function subscribeToPush() {
                if (!('PushManager' in window)) {
                    console.log('Push notifications not supported');
                    return;
                }
                
                navigator.serviceWorker.ready
                    .then((registration) => {
                        return registration.pushManager.subscribe({
                            userVisibleOnly: true,
                            applicationServerKey: 'YOUR_VAPID_PUBLIC_KEY'
                        });
                    })
                    .then((subscription) => {
                        console.log('Push subscription successful:', subscription);
                        // Send subscription to server
                        return fetch('/api/push/subscribe', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(subscription)
                        });
                    })
                    .catch((error) => {
                        console.error('Push subscription failed:', error);
                    });
            }
            
            // Subscribe on user action
            document.addEventListener('DOMContentLoaded', () => {
                const subscribeBtn = document.getElementById('subscribe-push');
                if (subscribeBtn) {
                    subscribeBtn.addEventListener('click', subscribeToPush);
                }
            });
        }
        """
    
    @staticmethod
    def get_push_notification_js() -> str:
        """
        Get push notification JavaScript.
        
        Returns:
            Push notification code
        """
        return """
        // Push Notification Functions
        function requestNotificationPermission() {
            if (!('Notification' in window)) {
                console.log('This browser does not support notifications');
                return;
            }
            
            Notification.requestPermission().then((permission) => {
                if (permission === 'granted') {
                    console.log('Notification permission granted!');
                    showNotification('Welcome to EcoBuddy AI! 🌱', 'Start your sustainability journey today!');
                }
            });
        }
        
        function showNotification(title, body) {
            if (Notification.permission === 'granted') {
                const options = {
                    body: body,
                    icon: '/static/icons/icon-192x192.png',
                    badge: '/static/icons/icon-72x72.png',
                    vibrate: [200, 100, 200]
                };
                
                new Notification(title, options);
            }
        }
        
        // Check if push is supported
        function isPushSupported() {
            return 'serviceWorker' in navigator && 'PushManager' in window;
        }
        """
    
    @staticmethod
    def get_offline_page() -> str:
        """
        Get offline fallback page HTML.
        
        Returns:
            Offline page HTML
        """
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EcoBuddy AI - Offline</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: #0f172a;
                    color: #f8fafc;
                    text-align: center;
                }
                .container {
                    max-width: 400px;
                    padding: 20px;
                }
                .icon {
                    font-size: 64px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #4ade80;
                    font-size: 24px;
                }
                p {
                    color: #94a3b8;
                    font-size: 16px;
                    line-height: 1.6;
                }
                .btn {
                    background: #4ade80;
                    color: #0f172a;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 20px;
                }
                .btn:hover {
                    background: #22c55e;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🌱</div>
                <h1>You're Offline</h1>
                <p>It looks like you're not connected to the internet.<br>
                Don't worry, EcoBuddy AI will be here when you're back online!</p>
                <button class="btn" onclick="window.location.reload()">🔄 Try Again</button>
            </div>
        </body>
        </html>
        """