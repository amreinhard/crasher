"use strict";

$.get('/process-json', function(results){
    initMap(results);
});

function initMap(results) {
    var eventMap = new google.maps.Map(document.getElementById('event-map'), {
        center: {lat: 37.7749, lng: -122.4194},
        styles: [
            {
                "stylers": [
                    {
                        "hue": "#707D7E"
                    },
                    {
                        "invert_lightness": true
                    },
                    {
                        "saturation": 0
                    },
                    {
                        "lightness": 20
                    },
                    {
                        "gamma": 0.5
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#12232B"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#D5ECEB"
                    }
                ]
            },
            {
                "featureType": 'administrative.locality',
                "elementType": 'labels.text.fill',
                "stylers": [
                    {
                        color: '#ded1cb'
                    }
                ]
            },
            {
                "featureType": 'poi',
                "elementType": 'labels.text.fill',
                "stylers": [
                    {
                        color: '#ded1cb'
                    }
                ]
            },
            {
                "featureType": 'poi.park',
                "elementType": 'geometry',
                "stylers": [{color: '#6C8F95'}]
            },
        ],
        scrollwheel: true,
        zoom: 12,
        zoomControl: false,
        panControl: true,
        streetViewControl: false,
    });

    for (var i = 0; i < results.length; i++) {
        if (results[i].hasOwnProperty("longitude") && results[i].hasOwnProperty('latitude')) {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(results[i].latitude, results[i].longitude),
                map: eventMap,
                title: "Event name:" + results[i].name
            });

            var eventPreview = (
            '<div class="window-content">' +
                '<p><b>Link: ' + '<a href="' + results[i].url + '">' + results[i].name + '</a></p>' +
                '<p><b>Location: </b>' + results[i].street + '</p>' +
                '<p><b>Event details: </b> <a href="/search-results/' + results[i].id + '">Link</a></p>' +
            '</div>');

            var infoWindow = new google.maps.InfoWindow({
                width: 150
            });

            bindInfoWindow(marker, eventMap, infoWindow, eventPreview);
        }
    }
    function bindInfoWindow(marker, eventMap, infoWindow, eventPreview) {
        google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(eventPreview);
          infoWindow.open(eventMap, marker);
        });
    }
}