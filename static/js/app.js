/**
 * Created by Peter.Makafan on 4/1/2016.
 */


var map;

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

    map = new google.maps.Map(document.getElementById('map-canvas'), options);
}


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


function search(query, callback) {

    var parameters = {
        name: query
    };
    $.getJSON("/search", parameters)
            .done(function (data, textStatus, jqXHR) {
                var results = data.houses;
                console.log(results)
                callback(results);
            })
            .fail(function (jqXHR, textStatus, errorThrown) {

                // log error to browser's console
                console.log(errorThrown.toString());
            });
}