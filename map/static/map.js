const osmAttribution = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osmLayer = L.tileLayer(osmUrl, { attribution: osmAttribution })
const map = L.map('map', { layers: [osmLayer] }).setView([51.17, 10.45], 7)

map.attributionControl.addAttribution('CORINE Land Cover Daten: © UBA')

async function loadPlz() {
    const plzUrl = `/map/api/plz/`
    const response = await fetch(plzUrl)
    const geojson = await response.json()
    return geojson
}
async function loadClcForPlz(plz) {
    const clcForPlzUrl = `/map/api/plz/${plz}/clc/`
    const response = await fetch(clcForPlzUrl)
    const json = await response.json()
    return json
}
async function renderPlz() {
    const plzGeojson = await loadPlz()
    const plzStyle = {
        'color': '#333',
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
    async function showPlz(e) {
        const layer = e.target
        map.fitBounds(layer.getBounds())
        const clcForPlz = await loadClcForPlz(layer.feature.properties.plz)
        plzDetails.update(layer.feature.properties, clcForPlz)
    }
    function onEachPlz(feature, layer) {
        layer.on({
            mouseover: highlightPlz,
            mouseout: resetHighlight,
            click: showPlz
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
            + props.population + ' Einwohner <br />'
            + Math.round(props.qkm) + ' km<sup>2</sup>'
            : 'Bewegen Sie den Mauszeiger auf ein Postleitzahlengebiet.')
    }
    plzInfo.addTo(map)

    // Use a custom control to show details for a PLZ.
    const plzDetails = L.control()
    plzDetails.setPosition('bottomright')
    plzDetails.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'plz-details')
        this.update()
        return this._div
    }
    plzDetails.update = function (props, clcForPlz) {
        function calcAggregatePercentage (aggregateSquareKilometers) {
            return Math.round(aggregateSquareKilometers / clcForPlz.plz_area_square_kilometers * 100)
        }
        this._div.innerHTML = '<h4>PLZ Details</h4>' + (props ?
            '<b>' + props.name + '</b><br />'
            + props.population + ' Einwohner <br />'
            + Math.round(props.qkm) + ' km<sup>2</sup> <br />'
            + calcAggregatePercentage(clcForPlz.aggregates_area_square_kilometers.aggregate_1) + ' % '
            + 'Nutzungscodes 100-199<br />'
            + calcAggregatePercentage(clcForPlz.aggregates_area_square_kilometers.aggregate_2) + ' % '
            + 'Nutzungscodes 200-299<br />'
            + calcAggregatePercentage(clcForPlz.aggregates_area_square_kilometers.aggregate_3) + ' % '
            + 'Nutzungscodes 300-399<br />'
            + calcAggregatePercentage(clcForPlz.aggregates_area_square_kilometers.aggregate_4) + ' % '
            + 'Nutzungscodes 400-499<br />'
            + calcAggregatePercentage(clcForPlz.aggregates_area_square_kilometers.aggregate_5) + ' % '
            + 'Nutzungscodes 500-599'
            : 'Klicken Sie auf ein Postleitzahlengebiet.')
    }
    plzDetails.addTo(map)
}

renderPlz()
