// Service Worker for ProjectMeats3 PWA
// Implements basic caching strategy for offline functionality

const CACHE_NAME = 'projectmeats3-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .catch((error) => {
        console.error('Service Worker: Cache failed', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        if (response) {
          console.log('Service Worker: Serving from cache:', event.request.url);
          return response;
        }

        // For API calls, try network first, then show offline message
        if (event.request.url.includes('/api/')) {
          return fetch(event.request)
            .catch(() => {
              // Return offline API response for critical endpoints
              if (event.request.url.includes('/tenant-theme/')) {
                return new Response(JSON.stringify({
                  tenant: 'Offline Mode',
                  theme: {
                    primary_color: '#2563eb',
                    secondary_color: '#64748b'
                  },
                  features: {
                    ai_assistant: true
                  }
                }), {
                  headers: { 'Content-Type': 'application/json' }
                });
              }
              
              return new Response(JSON.stringify({
                error: 'Offline - Please check your connection'
              }), {
                status: 503,
                headers: { 'Content-Type': 'application/json' }
              });
            });
        }

        // For other requests, fetch from network
        return fetch(event.request)
          .catch(() => {
            // Return offline page for navigation requests
            if (event.request.destination === 'document') {
              return caches.match('/');
            }
          });
      })
  );
});