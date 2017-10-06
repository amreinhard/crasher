"use strict";

$.get('/process-json', function(results){
    console.log(results);
    initMap(results);
});

function initMap(results) {
    console.log(results);
    var eventMap = new google.maps.Map(document.getElementById('event-map'), {
        center: {lat: results.latitude, lng: results.longitude},
        scrollwheel: true,
        zoom: 12,
        zoomControl: false,
        panControl: true,
        streetViewControl: false,
    });

    var infoWindow = new google.maps.InfoWindow({
        width: 150
  });

    function createMarker(results) {
        var marker;
       // for (var contents in results) {
            if (results.hasOwnProperty("longitude") && results.hasOwnProperty('latitude')) {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(results.latitude, results.longitude),
                    map: eventMap,
                    title: "Event name:" + results.event_name
                });

                var eventPreview = (
                    '<div class="window-content">' +
                        '<p><b>Event description: </b>' + results.event_description + '</p>' +
                        '<p><b>Location: </b>' + results.street + '</p>' +
                        '<p><b>Link: ' + '<a href="' + results.url + '">' + results.event_name + '</a></p>' +
                    '</div>');

                bindInfoWindow(marker, eventMap, infoWindow, eventPreview);
            }
    }

    createMarker(results);

    function bindInfoWindow(marker, eventMap, infoWindow, eventPreview) {
        google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(eventPreview);
          infoWindow.open(eventMap, marker);
      });
  }
}
