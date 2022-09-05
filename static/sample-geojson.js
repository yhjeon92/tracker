// Below are the custom-defined geoJSON objects.
// Source: https://aamoos.tistory.com/432

var map = L.map('map').setView([37.39903, 127.11152], 11);

const OSMUrlFormat = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const mapBoxUrlFormat = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
//const googleMapUrlFormat = 'https://mt0.google.com/vt/lyrs=m&hl=kr&x={x}&y={y}&z={z}';
const googleMapUrlFormat = 'http://192.168.35.116:8080/{x}_{y}_{z}.png';
const VWUrlFormat = 'http://xdworld.vworld.kr:8080/2d/Satellite/201612/{z}/{x}/{y}.jpeg'
const mapLayoutOptions = {
	minZoom: 8,
	maxZoom: 17,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox/light-v9',
	tileSize: 256,
	zoomOffset: 0,
	// tileSize: 512,
	// zoomOffset: -1,
	detectRetina: true
};

var mapLayer = L.tileLayer(OSMUrlFormat, mapLayoutOptions);
mapLayer.addTo(map);

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