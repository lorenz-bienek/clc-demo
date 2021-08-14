const osmAttribution = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osmLayer = L.tileLayer(osmUrl, { attribution: osmAttribution })
const map = L.map('map', { layers: [osmLayer] }).setView([51.17, 10.45], 7)

async function loadPlz() {
    const plzUrl = `/map/api/plz/`
    const response = await fetch(plzUrl)
    const geojson = await response.json()
    return geojson
}
async function renderPlz() {
    const plzGeojson = await loadPlz()
    const plzStyle = {
        'color': '#000000',
        'weight': 1,
        'fillOpacity': 0
    }

    function highlightPlz(e) {
        const layer = e.target
        layer.setStyle({
            weight: 2,
            fillOpacity: 0.1
        })
    }
    function resetHighlight(e) {
        geojsonLayer.resetStyle(e.target)
    }
    function onEachPlz(feature, layer) {
        layer.on({
            mouseover: highlightPlz,
            mouseout: resetHighlight
        })
    }

    const geojsonLayer = L.geoJSON(plzGeojson, {
        style: plzStyle,
        onEachFeature: onEachPlz
    }).addTo(map)
}
renderPlz()
