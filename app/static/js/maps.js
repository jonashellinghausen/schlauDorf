// Initialize Leaflet map
const map = L.map('map').setView([51.0, 10.0], 6);

// Base layer
const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// WMS layer via proxy
const wmsLayer = L.tileLayer.wms('/api/wms-proxy', {
  layers: 'default',
  format: 'image/png',
  transparent: true
});

// Layer control
const baseLayers = { 'OpenStreetMap': osm };
const overlays = { 'WMS Layer': wmsLayer };
L.control.layers(baseLayers, overlays).addTo(map);
