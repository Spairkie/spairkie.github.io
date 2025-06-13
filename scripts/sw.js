const CACHE_NAME = "portfolio-cache-v1";
const urlsToCache = [
  "/",
  
  "/index.html",
  "/style/style.css",
  "/scripts/main.js",

  "/bento.html",
  "/style/bento.css",
  
  "/style/theme.css",
  
  "/offline.html",

  "/headshot.jpeg",
  "/icons/icon-192.png",
  "/icons/icon-512.png"
];

// Install and cache files
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Clean up old caches
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      );
    })
  );
});

// Intercept fetch requests
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return (
        response ||
        fetch(event.request).catch(() => caches.match("/offline.html"))
      );
    })
  );
});
