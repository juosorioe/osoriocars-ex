
function initMap() {
    var location = { lat: -33.408784, lng: -70.567596 }; // Coordenadas para una dirección aleatoria en Las Condes, Chile
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: location
    });
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}