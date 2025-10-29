// Service Worker
const CACHE_NAME = 'biophysio-consultant-v3';
const urlsToCache = [
  '/',
  '/static/js/app.js',
  '/static/images/pratap.jpeg',
  '/manifest.json',
  '/static/images/icon-192x192.png',
  '/static/images/icon-512x512.png',
  '/static/images/loogoo.png'
];

// Get base URL for handling both localhost and IP address
const getBaseUrl = () => {
  return self.location.origin;
};

// Clear old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

self.addEventListener('install', event => {
  // Force waiting service worker to become active
  self.skipWaiting();
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request)
          .then(response => {
            // Check if we received a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          });
      })
  );
});