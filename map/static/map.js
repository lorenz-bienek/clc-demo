const osmAttribution = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osmLayer = L.tileLayer(osmUrl, { attribution: osmAttribution })
const map = L.map('map', { layers: [osmLayer] }).setView([51.17, 10.45], 7)
