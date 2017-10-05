function initMap() {
    var eventMap = new google.maps.Map(document.getElementById('event-map'), {
        center: {lat: 37.7400, lng: -122.4100},
        scrollwheel: true,
        zoom: 12,
        zoomControl: false,
        panControl: true,
        streetViewControl: false,
    });

    var infoWindow = new google.maps.InfoWindow({
    width: 150
  });
// open, read, turn into json obj


    function readJSON(file) {
        var marker;
        for (var contents in results) {
            if (contents.hasOwnProperty('longitude') && contents.hasOwnProperty('latitude')) {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(contents.latitude, contents.longitude),
                    map: eventMap,
                    title: "Event name:" + contents.event_name
                });

                eventPreview = (
                    '<div class="window-content">' +
                        '<p><b>Event description:</b>' + contents.event_description + '</p>' +
                        '<p><b>Location</b>' + contents.street + '</p>' +
                        '<p><b>Link: ' + '<a href="' + contents.url + '">' + contents.event_name + '</a></p>' +
                    '</div>');

                bindInfoWindow(marker, eventMap, infoWindow, eventPreview);
            }
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