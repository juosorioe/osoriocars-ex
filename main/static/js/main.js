//Mapa
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

$(document).ready(function() {
    $('.view-message').on('click', function() {
        var messageId = $(this).data('id');
        
        // Fetch message details via AJAX
        $.ajax({
            url: '/admin_dashboard/get_contact_message/' + messageId + '/',
            method: 'GET',
            success: function(data) {
                $('#contactMessageModal .modal-body').html(`
                    <p><strong>Nombre:</strong> ${data.name}</p>
                    <p><strong>Correo:</strong> ${data.email}</p>
                    <p><strong>Asunto:</strong> ${data.subject}</p>
                    <p><strong>Mensaje:</strong> ${data.message}</p>
                `);
                $('#delete-message-id').val(messageId);
                $('#contactMessageModal').modal('show');
            },
            error: function() {
                alert('Error al cargar el mensaje');
            }
        });
    });

    $('#delete-contact-message-form').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            success: function() {
                $('#contactMessageModal').modal('hide');
                location.reload(); // Recargar la página para ver los cambios
            },
            error: function() {
                alert('Error al eliminar el mensaje');
            }
        });
    });
});