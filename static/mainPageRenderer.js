document.getElementById('title').innerHTML = titleString;
const changeMapType = () => {
    var typeSelect = document.getElementById("mapType");
    var selectedValue = typeSelect.options[typeSelect.selectedIndex].value;
    switch (selectedValue) {
        case 'openstreetmap':
            console.log(selectedValue);
            map.removeLayer(mapLayer);
            mapLayoutOptions['attribution'] = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
            mapLayer = L.tileLayer(OSMUrlFormat, mapLayoutOptions);
            mapLayer.redraw();
            mapLayer.addTo(map);
            break;
        case 'mapbox':
            console.log(selectedValue);
            map.removeLayer(mapLayer);
            mapLayer = L.tileLayer(mapBoxUrlFormat, mapLayoutOptions);
            mapLayer.redraw();
            mapLayer.addTo(map);
            break;
        case 'google':
            console.log(selectedValue);
            map.removeLayer(mapLayer);
            mapLayoutOptions['attribution'] = 'Map data &copy; <a href="https://www.google.com/maps">Google Maps</a>';
            mapLayer = L.tileLayer(googleMapUrlFormat, mapLayoutOptions);
            mapLayer.redraw();
            mapLayer.addTo(map);
            break;
        case 'vw':
            console.log(selectedValue);
            map.removeLayer(mapLayer);
            mapLayoutOptions['attribution'] = 'Map data &copy; <a href="https://vworld.kr">VWorld Korea</a>';
            mapLayer = L.tileLayer(VWUrlFormat, mapLayoutOptions);
            mapLayer.redraw();
            mapLayer.addTo(map);
    }
};

pointCoordinates = trail['features'][0]['geometry']['coordinates'];
var showDetail = false;
var showMarker = true;
const redrawMap = () => {
    document.getElementById('title').innerHTML = titleString;
    showDetail = !showDetail;
    trail['features'][0]['properties']['underConstruction'] = showDetail;

    map.removeLayer(L.geoJSON);
    trailLayer.clearLayers();
    trailLayer = L.geoJSON(trail, {
        filter: function (feature, layer) {
            if (feature.properties) {
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

    pointLayer.clearLayers();
    pointLayer = L.geoJSON(points, {
        onEachFeature: onEachFeature,

        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
                radius: 3,
                fillColor: "#2a2aff",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            });
        }
    });

    if (showDetail) {
        pointLayer.addTo(map);
    }
}

const redrawMarker = () => {
    showMarker = !showMarker;
    featureCount = trail['features'].length;
    for (let i = 1; i < featureCount; i++) {
        trail['features'][i]['properties']['underConstruction'] = !showMarker;
    }

    map.removeLayer(L.geoJSON);
    trailLayer.clearLayers();
    trailLayer = L.geoJSON(trail, {
        filter: function (feature, layer) {
            if (feature.properties) {
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
}

const resetView = () => {
    if (points['features'].length > 1) {
        var yxcoord = points['features'][0]['geometry']['coordinates']
        map.setView([yxcoord[1], yxcoord[0]], 11);
    } else {
        map.setView([37.39903, 127.11152], 11);
    }
    
}
document.getElementById('resetView').onclick = resetView;
document.getElementById('toggleDetail').onclick = redrawMap;
document.getElementById('toggleMarker').onclick = redrawMarker;

var singlePoint = L.geoJSON();

const drawSingle = (featureSingle) => {
    singlePoint.clearLayers();
    singlePoint = L.geoJSON(
        {
            type: "FeatureCollection",
            features: [
                featureSingle
            ]
        }, 
        {
            onEachFeature: onEachFeature,
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: 7,
                    fillColor: "#ff2222",
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            }
        }
    );
    singlePoint.addTo(map);
}

workoutPlot = document.getElementById('workoutPlot');
var plot_data = [
    {
        name: 'Elevation (m)',
        x: distance,
        y: elevation,
        yaxis: 'y2',
        line: {
            color: 'rgb(225, 225, 225)',
            width: 1
        },
        fill: 'tozeroy',
        type: 'scatter',
    },
    {
        name: 'Speed',
        x: distance,
        y: velocity,
        line: {
            shape: 'spline',
            smoothing: 1.5
        },
        mode: 'lines',
        type: 'scatter'
    },
];

var plot_layout = {
    margin: { t: 0 },
    hovermode:'closest',
    xaxis: {
        title: {
            text: "Distance (km)",
            font: {
                family: "Courier New, monospace",
                size: 18,
                color: "#7f7f7f"
            }
        }
    },
    yaxis: {
        title: {
            text: "Speed (km/h)",
            font: {
                family: "Courier New, monospace",
                size: 18,
                color: "#7f7f7f"
            }
        },
        rangemode: 'tozero'
    },
    yaxis2: {
        title: 'Elevation(m)',
        titlefont: { color: 'rgb(148, 103, 189)' },
        tickfont: { color: 'rgb(148, 103, 189)' },
        overlaying: 'y',
        rangemode: 'tozero',
        side: 'right'
    }
};

Plotly.newPlot(workoutPlot, plot_data, plot_layout);
const redrawWorkoutPlot = (dist_new, time_new, elev_new, velo_new) => {
    if (document.getElementById("plotAxisToggle").value === "To distance") {
        plot_data[0]['x'] = time_new;
        plot_data[1]['x'] = time_new;
    } else {
        plot_data[0]['x'] = dist_new;
        plot_data[1]['x'] = dist_new;
    }
    plot_data[0]['y'] = elev_new;
    plot_data[1]['y'] = velo_new;
    Plotly.redraw(workoutPlot);
}

workoutPlot.on('plotly_hover', function(data){
    var index = data.points.map(function(d) { return d.pointNumber });
    var featureSinglePoint = points['features'][index];
    drawSingle(featureSinglePoint);
}).on('plotly_unhover', function(data){
    singlePoint.clearLayers();
});

const toTimestamp = () => {
    plot_data[0]['x'] = timestamp;
    plot_data[1]['x'] = timestamp;
    plot_layout['xaxis']['title']['text'] = 'Time'
    Plotly.restyle(workoutPlot, 'x', [timestamp]);

    document.getElementById("plotAxisToggle").value = "To distance";
    document.getElementById("plotAxisToggle").onclick = toDistance;
}
const toDistance = () => {
    plot_data[0]['x'] = distance;
    plot_data[1]['x'] = distance;
    plot_layout['xaxis']['title']['text'] = 'Distance (km)'
    Plotly.restyle(workoutPlot, 'x', [distance]);

    document.getElementById("plotAxisToggle").value = "To timestamp";
    document.getElementById("plotAxisToggle").onclick = toTimestamp;
}
document.getElementById("plotAxisToggle").onclick = toTimestamp;


const submitButton = document.getElementById("submitButton");

document.getElementById("fileProfile").onchange = () => {
    console.log(document.getElementById("fileProfile").files[0]);
}

const submit = () => {
    var form = document.getElementById("fileUploadForm");
    var inputFile = document.getElementById("fileProfile");

    console.log(inputFile.files.length);
    if (inputFile.files.length > 0) {
        var formData = new FormData();
        formData.append('file', inputFile.files[0]);
        fetch("/upload", {
            method: "POST",
            body: formData
        }).then(res => res.json())
            .then(res => {
                titleString = res['titleString'];
                points = res['points'];
                trail = res['trail'];
                timestamp = res['timestamp'];
                distance = res['distance'];
                elevation = res['elevation'];
                velocity = res['velocity'];
                redrawMap();
                redrawMarker();
                redrawMap();
                redrawMarker();
                resetView();
                redrawWorkoutPlot(distance, timestamp, elevation, velocity);

                // console.log(res.message);
                // let scriptEle = document.createElement("script");
                // document.body.appendChild(scriptEle);
                // scriptEle.setAttribute("src", "/" + res.message);
                // scriptEle.setAttribute("type", "text/javascript");
            }).catch((error) => ("Something went wrong!", error));
    };
};
submitButton.onclick = submit;
