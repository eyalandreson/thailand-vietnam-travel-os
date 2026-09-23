// Service Worker: Adaptive Travel OS Offline Resilience Engine (v4.8)
const CACHE_NAME = 'travel-os-v4.8';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './styles.css?v=4.8',
  './config.js?v=4.8',
  './app.js?v=4.8&b=2026092308',
  './itinerary_data.js?v=4.8',
  './data.json',
  './master_itinerary_doc.html',
  './manifest.json',
  './documents/Emirates_Flight_TLV_BKK_G5M8CF.pdf',
  './documents/TDAC_Arrival_Card_30C4358.pdf',
  './documents/Sukhon_Hotel_Agoda_697155847.pdf',
  './documents/Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf',
  './documents/Etihad_BKK_TLV_9KDEH2_Eyal_Andreson.pdf',
  './documents/Etihad_BKK_TLV_9KDEH2_Maria_Miriam_Malayev.pdf',
  './documents/12go_booking_32785393.pdf',
  './documents/Confirmation_for_Booking_ID__1777345669.pdf',
  './documents/Confirmation_for_Booking_ID__1777544987.pdf',
  './documents/Confirmation_for_Booking_ID__2050574832.pdf',
  './documents/Confirmation_for_Booking_ID__2050577065.pdf',
  './documents/Confirmation_for_Booking_ID__2051512276.pdf',
  './documents/Confirmation_for_Booking_ID__2051965881.pdf',
  './documents/Confirmation_for_Booking_ID__697155847.pdf',
  './documents/Travel Reservation 24SEP for EYAL ANDRESON.pdf',
  './documents/Your flight information - BANGKOK AIRWAYS.pdf',
  './documents/20260923010739842_842708495_96485234.pdf',
  './documents/Voucher_34GR92_Vexere Confirmation of successful  payme.html',
  './documents/Voucher_E8PB24_Vexere Confirmation of successful  payme.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW v4.5] Pre-caching offline Travel OS assets and PDF documents');
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.warn('[SW v4.3] Cache addAll warning:', err);
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
            console.log('[SW v4.0] Clearing stale cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    }).then(() => {
      // Force all active client tabs to reload with fresh v4.0 assets
      return self.clients.matchAll({ type: 'window' });
    }).then((clients) => {
      if (clients && clients.length > 0) {
        clients.forEach((client) => {
          client.postMessage({ action: 'RELOAD_PAGE', version: CACHE_NAME });
        });
      }
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Pass through non-GET requests (e.g. POST to Gemini API) and cross-origin calls directly to network
  if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
    return;
  }

  // Network-First Strategy for HTML, JS, CSS, JSON:
  // When online, ALWAYS serve the newest version from server and update cache.
  // Fallback to cache ONLY when offline.
  event.respondWith(
    fetch(event.request)
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
        // Device is offline: fallback to cached assets
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
  );
});