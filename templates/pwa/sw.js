// Service Worker for Bio-Physio Consultant PWA
const CACHE_NAME = 'healthcare-booking-v1';
const urlsToCache = [
  '/',
  '/static/js/app.js',
  '/static/images/loogoo.png',
  '/offline/',
];

// Install Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch events
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        
        return fetch(event.request).catch(function() {
          // Return offline page for navigation requests
          if (event.request.mode === 'navigate') {
            return caches.match('/offline/');
          }
        });
      }
    )
  );
});

// Activate Service Worker
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Handle push notifications (if implemented in future)
self.addEventListener('push', function(event) {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body,
      icon: '/static/images/loogoo.png',
      badge: '/static/images/loogoo.png',
      vibrate: [200, 100, 200],
      data: {
        url: data.url || '/'
      },
      actions: [
        {
          action: 'view',
          title: 'View',
          icon: '/static/images/loogoo.png'
        },
        {
          action: 'close',
          title: 'Close',
          icon: '/static/images/loogoo.png'
        }
      ]
    };

    event.waitUntil(
      self.registration.showNotification(data.title, options)
    );
  }
});

// Handle notification clicks
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow(event.notification.data.url)
    );
  }
});