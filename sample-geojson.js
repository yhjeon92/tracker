// Below are the custom-defined geoJSON objects.
// Source: https://aamoos.tistory.com/432

var map = L.map('map').setView([37.39903, 127.11152], 11);

const terrainMapUrlFormat = 'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png';
const roadMapUrlFormat = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
// const naverMapUrlFormat = 'https://map.pstatic.net/nrb/styles/basic/1655974504/{z}/{x}/{y}.png'
const naverMapUrlFormat = 'https://a.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png';
const mapLayoutOptions = {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox/light-v9',
	tileSize: 512,
	zoomOffset: -1,
	detectRetina: true
};

var mapLayer = L.tileLayer(roadMapUrlFormat, mapLayoutOptions).addTo(map);

function onEachFeature(feature, layer) {
	var popupContent = "<p>Powered by GeoJSON and Leaflet</p>";

	if (feature.properties && feature.properties.popupContent) {
		popupContent += feature.properties.popupContent;
	}

	layer.bindPopup(popupContent);
}

var trailLayer = L.geoJSON(trail, {
	filter: function (feature, layer) {
		if (feature.properties) {
			// If the property "underConstruction" exists and is true, return false (don't render features under construction)
			return feature.properties.underConstruction !== undefined ? !feature.properties.underConstruction : true;
		}
		return false;
	},

	onEachFeature: onEachFeature,
	
	pointToLayer: function (feature, latlng) {
 		return L.circleMarker(latlng, {
 			radius: 4,
 			fillColor: "#ff2a2a",
 			color: "#000",
 			weight: 1,
			opacity: 1,
 			fillOpacity: 0.8
 		});
 	}
});

trailLayer.addTo(map);

var pointLayer = L.geoJSON();