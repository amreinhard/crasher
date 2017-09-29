function initMap() {
    var eventMap = new google.maps.Map(document.getElementById('event-map'), {
        scrollwheel: false,
        zoom: 7,
        zoomControl: true,
        panControl: true,
        streetViewControl: false,
    });

    var infoWindow = new google.maps.InfoWindow({
    width: 150
  });

    $.get('/event-results.json', function(results) {
        var marker;
        for (var contents in results) {
            if (results.hasOwnProperty('longitude') && results.hasOwnProperty('latitude')) {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(results.latitude, results.longitude),
                    map: eventMap,
                    title: "Event name:" + results.event_name
                });

                eventPreview = (
                    '<div class="window-content">' +
                        '<p><b>Event description:</b>' + results.event_description + '</p>' +
                        '<p><b>Location</b>' + results.street + '</p>' +
                        '<p><b>Link: ' + '<a href="' + results.url + '">' + results.event_name + '</a></p>' +
                    '</div>');

                bindInfoWindow(marker, eventMap, infoWindow, eventPreview);
            }
        }
    });

    function bindInfoWindow(marker, eventMap, infoWindow, eventPreview) {
        google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(eventPreview);
          infoWindow.open(eventMap, marker);
      });
  }
}

google.maps.event.addDomListener(window, 'load', initMap);