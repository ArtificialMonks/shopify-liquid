/**
 * Service Worker for Theme Performance Optimization
 * Handles caching, offline functionality, and performance improvements
 */

const CACHE_NAME = 'shopify-theme-v1';
const STATIC_CACHE = 'static-v1';
const DYNAMIC_CACHE = 'dynamic-v1';

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/collections',
  '/pages/about',
  '/pages/contact'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');

  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .catch((error) => {
        console.error('Error caching static assets:', error);
      })
  );

  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => {
              return cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE;
            })
            .map((cacheName) => {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
  );

  self.clients.claim();
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip external requests
  if (url.origin !== location.origin) {
    return;
  }

  // Skip cart and checkout pages
  if (url.pathname.includes('/cart') || url.pathname.includes('/checkout')) {
    return;
  }

  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        // Return cached version if available
        if (cachedResponse) {
          console.log('Serving from cache:', request.url);
          return cachedResponse;
        }

        // Fetch from network and cache
        return fetch(request)
          .then((networkResponse) => {
            // Check if response is valid
            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              return networkResponse;
            }

            // Clone response for caching
            const responseToCache = networkResponse.clone();

            // Determine cache based on content type
            const contentType = networkResponse.headers.get('content-type');
            let targetCache = DYNAMIC_CACHE;

            if (contentType && (
              contentType.includes('text/css') ||
              contentType.includes('application/javascript') ||
              contentType.includes('image/')
            )) {
              targetCache = STATIC_CACHE;
            }

            // Cache the response
            caches.open(targetCache)
              .then((cache) => {
                console.log('Caching:', request.url);
                cache.put(request, responseToCache);
              })
              .catch((error) => {
                console.error('Error caching response:', error);
              });

            return networkResponse;
          })
          .catch((error) => {
            console.error('Fetch failed:', error);

            // Return offline page for navigation requests
            if (request.destination === 'document') {
              return caches.match('/offline.html');
            }

            // Return placeholder for images
            if (request.destination === 'image') {
              return new Response(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="#f0f0f0"/><text x="50%" y="50%" text-anchor="middle" dy=".3em">Offline</text></svg>',
                { headers: { 'Content-Type': 'image/svg+xml' } }
              );
            }

            throw error;
          });
      })
  );
});

// Background sync for form submissions (if supported)
if ('sync' in self.registration) {
  self.addEventListener('sync', (event) => {
    console.log('Background sync triggered:', event.tag);

    if (event.tag === 'newsletter-signup') {
      event.waitUntil(processNewsletterSignups());
    }

    if (event.tag === 'contact-form') {
      event.waitUntil(processContactForms());
    }
  });
}

// Process queued newsletter signups
async function processNewsletterSignups() {
  try {
    const cache = await caches.open('form-data');
    const requests = await cache.keys();

    for (const request of requests) {
      if (request.url.includes('newsletter')) {
        try {
          await fetch(request);
          await cache.delete(request);
          console.log('Newsletter signup processed');
        } catch (error) {
          console.error('Failed to process newsletter signup:', error);
        }
      }
    }
  } catch (error) {
    console.error('Error processing newsletter signups:', error);
  }
}

// Process queued contact forms
async function processContactForms() {
  try {
    const cache = await caches.open('form-data');
    const requests = await cache.keys();

    for (const request of requests) {
      if (request.url.includes('contact')) {
        try {
          await fetch(request);
          await cache.delete(request);
          console.log('Contact form processed');
        } catch (error) {
          console.error('Failed to process contact form:', error);
        }
      }
    }
  } catch (error) {
    console.error('Error processing contact forms:', error);
  }
}

// Push notification handling (if supported)
if ('push' in self.registration) {
  self.addEventListener('push', (event) => {
    console.log('Push notification received');

    let data = {};

    if (event.data) {
      try {
        data = event.data.json();
      } catch (error) {
        data = { title: 'Notification', body: event.data.text() };
      }
    }

    const options = {
      title: data.title || 'New Update',
      body: data.body || 'You have a new notification',
      icon: data.icon || '/assets/icon-192.png',
      badge: data.badge || '/assets/badge-72.png',
      tag: data.tag || 'default',
      requireInteraction: data.requireInteraction || false,
      actions: data.actions || []
    };

    event.waitUntil(
      self.registration.showNotification(options.title, options)
    );
  });

  self.addEventListener('notificationclick', (event) => {
    console.log('Notification clicked');

    event.notification.close();

    const clickAction = event.action || 'default';
    let targetUrl = '/';

    if (event.notification.data && event.notification.data.url) {
      targetUrl = event.notification.data.url;
    }

    event.waitUntil(
      clients.matchAll({ type: 'window' })
        .then((clientList) => {
          for (const client of clientList) {
            if (client.url === targetUrl && 'focus' in client) {
              return client.focus();
            }
          }

          if (clients.openWindow) {
            return clients.openWindow(targetUrl);
          }
        })
    );
  });
}

// Handle messages from main thread
self.addEventListener('message', (event) => {
  console.log('Service Worker received message:', event.data);

  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(DYNAMIC_CACHE)
        .then((cache) => {
          return cache.addAll(event.data.urls);
        })
    );
  }
});