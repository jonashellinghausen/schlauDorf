// Initialize Leaflet map with WMS layer via /api/wms-proxy

document.addEventListener('DOMContentLoaded', function () {
  const map = L.map('map').setView([0, 0], 2);

  // Base layer from OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Example WMS layer fetched through the proxy
  L.tileLayer.wms('/api/wms-proxy', {
    layers: 'example',
    format: 'image/png',
    transparent: true
  }).addTo(map);
});
