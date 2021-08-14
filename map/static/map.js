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
        plzInfo.update(layer.feature.properties)
    }
    function resetHighlight(e) {
        geojsonLayer.resetStyle(e.target)
        plzInfo.update()
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

    // Use a custom control to show information about a PLZ.
    const plzInfo = L.control()
    plzInfo.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'plz-info')
        this.update()
        return this._div
    }
    plzInfo.update = function (props) {
        this._div.innerHTML = '<h4>PLZ Info</h4>' +  (props ?
            '<b>' + props.name + '</b><br />'
            + props.population + ' Einwohner' + '<br />'
            + Math.round(props.qkm) + ' km<sup>2</sup>'
            : 'Bewegen Sie den Mauszeiger auf ein Postleitzahlengebiet.')
    }
    plzInfo.addTo(map)
}

renderPlz()
