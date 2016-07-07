/**
 * Created by Peter.Makafan on 4/1/2016.
 */



var map;
var markers = [];


function initMap() {


    var styles = [{
        featureType: "poi",
        elementType: "labels",
        stylers: [{
            visibility: "off"
        }]
    }];


    var options = {
        center: {lat: 6.4705912, lng: 3.5674984},
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 14,
        panControl: false,
        styles: styles,
        zoom: 25,
        zoomControl: true,
        scrollwheel: true
    };

      // get DOM node in which map will be instantiated
    var canvas = document.getElementById('map-canvas');

    // instantiate map
    map = new google.maps.Map(canvas, options);

    // configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);
}

var configure  = function () {
      google.maps.event.addListener(map, "dragend", function () {
        update();
    });

    // update UI after zoom level changes
    google.maps.event.addListener(map, "zoom_changed", function () {
        update();
    });

    // remove markers whilst dragging
    google.maps.event.addListener(map, "dragstart", function () {
        removeMarkers();
    });

    $("#search").typeahead({
        autoselect: true,
        highlight: true,
        minLength: 1
    },
    {
        source: search,
        templates: {
            empty:"Noting O",
            suggestion: _.template("<a class=''> <%- name %></a>")
        }
    });


    // re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
    // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
    document.addEventListener("contextmenu", function (event) {
        event.returnValue = true;
        event.stopPropagation && event.stopPropagation();
        event.cancelBubble && event.cancelBubble();
    }, true);

    // update UI
    update();

    // give focus to text box
    $("#search").focus();
};




function search(query, callback) {

    var parameters = {
        name: query
    };
    $.getJSON("/search", parameters)
            .done(function (data, textStatus, jqXHR) {
                var results = data.houses;
                console.log(results);
                callback(results);
            })
            .fail(function (jqXHR, textStatus, errorThrown) {

                // log error to browser's console
                console.log(errorThrown.toString());
            });
}


var removeMarkers = function() {
      for (var i = 0; i < markers.length; i++) {
        if (markers[i]) {
            markers[i].setMap(null);
            markers[i] = null;
        }
    }
}
var addMarker = function (data) {
    var newMarker = new google.maps.Marker({
        position: new google.maps.LatLng(data.latitude, data.longitude),
        animation: google.maps.Animation.DROP,
        map: map,
    });

      markers.push(newMarker);
};
/**
 *
 * Updates UI's markers.
 */
var  update = function()
{
    // get map's bounds
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();

    // get places within bounds (asynchronously)
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#search").val(),
        sw: sw.lat() + "," + sw.lng()
    };
    $.getJSON("update", parameters)
            .done(function (data, textStatus, jqXHR) {

                // remove old markers from map
                removeMarkers();
                var houses = data.houses || [];
                // add new markers to map
                for (var i = 0; i < houses.length; i++)
                {
                    addMarker(houses[i]);
                    console.log(houses[i]);
                }
            })
            .fail(function (jqXHR, textStatus, errorThrown) {

                // log error to browser's console
                console.log(errorThrown.toString());
            });
};