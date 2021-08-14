const osmAttribution = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osmLayer = L.tileLayer(osmUrl, { attribution: osmAttribution })
const map = L.map('map', { layers: [osmLayer] }).setView([51.17, 10.45], 7)

async function load_plz() {
    const plzUrl = `/map/api/plz/`
    const response = await fetch(plzUrl)
    const geojson = await response.json()
    return geojson
}
async function render_plz() {
    const plzGeojson = await load_plz()
    const plzStyle = {
        'color': '#000000',
        'weight': 1,
        'fill': false
    }
    L.geoJSON(plzGeojson, {
        style: plzStyle
    }).addTo(map)
}
render_plz()
