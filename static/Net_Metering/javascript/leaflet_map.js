// Map
var southWest = L.latLng(30, 15); // SW corner (between Africa and Balkans)
var northEast = L.latLng(45, 32); // NE corner (between Italy, and Turkey)
var bounds = L.latLngBounds(southWest, northEast); // LatLngBounds object
let map = L.map('map').setView([37.983917, 23.72936], 7);
let latitude = document.getElementById('latitude')
let longitude = document.getElementById('longitude')
// Get the region input element
let regionInput = document.getElementById('regionInput');
let geojsonLayer;

// Set the maximum bounds for the map after initialization
map.setMaxBounds(bounds);

// When the map moves --> end of the bounds,returns to center coords
map.on('moveend', function () {
    var center = map.getCenter();
  
    // Check if the map's center longitude has wrapped around
    if (center.lng < -180 || center.lng > 180) {
      // Re-add your layer or perform any other actions you need
      // Example: map.addLayer(yourLayer);
      console.log('Map has wrapped around');
    }
});

// 1st layer, the map itself
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Creating Marker options
var markerOptions = {
    title: "MyLocation",
    clickable: true,
}
// Creating a marker
let marker = L.marker([37.983917, 23.72936], markerOptions);

// Adding marker to the map
marker.addTo(map);

//Function to add text popup, prefecture identifier layer 
function popUp(feature, layer) {
    if (feature.properties) {
        const propertiesToShow = ['ΝΟΜΟΣ', 'ΕΔΡΑ', 'ΠΛΗΘΥΣΜΟΣ'];
        const out = propertiesToShow.map(key => {
            let value = feature.properties[key];
            if (key === 'NAME') {
                value = decodeURIComponent(value);
            }
            return key + ': ' + value;
        });
        layer.bindPopup(out.join('<br />'));
    }
};

// Function to check if a point is inside a polygon using Turf.js
function isPointInsidePolygon(lng, lat, polygon) {
    const turfPoint = turf.point([lng, lat]);
    const turfPolygon = turf.polygon(polygon);
    return turf.booleanPointInPolygon(turfPoint, turfPolygon);
};

function onMapClick(e) {
    latitude.value = e.latlng.lat.toFixed(4);
    longitude.value = e.latlng.lng.toFixed(4);
    console.log(latitude.value);
    console.log(longitude.value);

    let isPointOutsideBounds = true;

    if (geojsonLayer) {
        geojsonLayer.eachLayer(layer => {
            const geometryType = layer.feature.geometry.type;
            const polygons = layer.feature.geometry.coordinates;
        
            if (geometryType === 'MultiPolygon') { 
                polygons.forEach(polygon => {
                    if ( isPointInsidePolygon(longitude.value, latitude.value, polygon) ) {
                        console.log(layer.feature.properties.ΝΟΜΟΣ);
                        regionInput.value = layer.feature.properties.ΝΟΜΟΣ;
                        placeSelected.value = regionInput.value;
                        triggerButtonEnable();    
    
                        //layer.openPopup();
                        isPointOutsideBounds = false;
                         // Remove the existing marker from the map
                        if (marker) {
                            marker.remove();
                        }
                        // Create a new marker at the clicked position
                        marker = L.marker([latitude.value, longitude.value]).addTo(map);
                    }
                });
            }
        });
    };

    if (isPointOutsideBounds) {
        latitude.value = '';
        longitude.value = '';
        regionInput.value = ''; // Clear the region input if the point is outside polygons
        marker.remove();
        triggerButtonDisable();
    };
};

// 2nd layer reading GeoJSON data
fetch(geojsonPath)
    .then(response => response.json())
    .then(geoJsonData => {
       geojsonLayer = L.geoJSON(geoJsonData, {
            onEachFeature: popUp }
        );
        
        geojsonLayer.addTo(map);
        // map.fitBounds(geojsonLayer.getBounds());

        const transparentLayer = L.geoJSON(geoJsonData, {
            style: {
                fillOpacity: 0,
                interactive: true,
                strokeOpacity: 0,
            },
        });
        
        transparentLayer.addTo(map);

        map.on('click', onMapClick);

    });


    

