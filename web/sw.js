// Service Worker: Adaptive Travel OS Offline Resilience Engine
const CACHE_NAME = 'travel-os-v3.1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './itinerary_data.js',
  './data.json',
  './master_itinerary_doc.html',
  './manifest.json',
  './documents/Emirates_Flight_TLV_BKK_G5M8CF.pdf',
  './documents/TDAC_Arrival_Card_30C4358.pdf',
  './documents/Sukhon_Hotel_Agoda_697155847.pdf',
  './documents/Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf',
  './documents/Etihad_BKK_TLV_9KDEH2_Eyal_Andreson.pdf',
  './documents/Etihad_BKK_TLV_9KDEH2_Maria_Miriam_Malayev.pdf'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Pre-caching offline Travel OS assets and PDF documents');
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.warn('[SW] Cache addAll warning:', err);
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[SW] Clearing stale cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // Stale-While-Revalidate strategy for app shell and assets
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // If offline and requesting navigation, fallback to cached index.html
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });

      return cachedResponse || fetchPromise;
    })
  );
});