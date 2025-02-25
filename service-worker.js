const cacheName = 'box-breathing-app-v1';
const assets = [
  'index.html',
  'main.py',
  'manifest.json',
  // Include PyScript assets
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(cacheName)
      .then(cache => {
        return cache.addAll(assets);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
