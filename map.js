function loadJSON(callback) {   
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', 'ffl-list-pennsylvania.json', true);
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
      callback(xobj.responseText);
    }
  };
  xobj.send(null);  
}

function loadMarkerIcon(color) {
  return new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-' + color + '.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
}

function createMap(fflsJson) {
  var greenIcon = loadMarkerIcon('green');
  var yellowIcon = loadMarkerIcon('yellow');
  var redIcon = loadMarkerIcon('red');
  var grayIcon = loadMarkerIcon('grey');

  /** Coordinates are decimal degree coords **/
  var fflMap = L.map('mapid').setView([40.5773, -77.264], 7);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
      '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
  }).addTo(fflMap);

  ffls = JSON.parse(fflsJson).ffls;
  for (var i in ffls) {
    ffl = ffls[i];

    var icon;
    if (ffl.status == 'joined') {
      icon = greenIcon;
    } else if (ffl.status == 'contacted') {
      icon = yellowIcon;
    } else if (ffl.status == 'rejected') {
      icon = redIcon;
    } else {
      icon = grayIcon;
    }

    fflMarker = L.marker([ffl.lat, ffl.lon], {
      icon: icon
    }).addTo(fflMap);

    hasUrl = ffl.url !== "";
    namePart = "";
    if (hasUrl) {
      namePart = '<a href="' + ffl.url + '">' + ffl.businessName + '</a>';
    } else {
      namePart = ffl.businessName;
    }

    fflMarker.bindPopup(namePart + '<br>' + ffl.address + '<br>' + ffl.phone + '<br>Status: ' + ffl.status);
  }
}

loadJSON(createMap);
