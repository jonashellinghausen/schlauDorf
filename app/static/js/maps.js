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
const layerControl = L.control.layers(baseLayers, overlays).addTo(map);

// Load GPX tracks and add to map
fetch('/api/gpx/tracks')
  .then(response => response.json())
  .then(tracks => {
    tracks.forEach(track => {
      const geoLayer = L.geoJSON(track.geometry);
      let popup = `<strong>${track.name}</strong>`;
      const extras = [];
      if (track.distance_km !== null) extras.push(`${track.distance_km} km`);
      if (track.elevation_gain_m !== null) extras.push(`${track.elevation_gain_m} m`);
      if (extras.length) {
        popup += `<br>${extras.join(', ')}`;
      }
      geoLayer.bindPopup(popup);
      geoLayer.addTo(map);
      layerControl.addOverlay(geoLayer, track.name);
    });
  })
  .catch(err => console.error('Error loading tracks', err));
