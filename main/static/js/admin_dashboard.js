$(document).ready(function() {
    $('.edit-user').on('click', function() {
        var userId = $(this).data('id');
        // Realizar la solicitud AJAX para obtener la información del usuario y mostrar el modal
        $.ajax({
            url: '/admin_dashboard/edit_user/' + userId + '/',
            method: 'GET',
            success: function(data) {
                $('#editUserId').val(data.id);
                $('#editUsername').val(data.username);
                $('#editEmail').val(data.email);
                $('#editRole').val(data.role);
                $('#editUserModal').modal('show');
            }
        });
    });

    $('#editUserForm').on('submit', function(event) {
        event.preventDefault();
        var userId = $('#editUserId').val();
        var formData = $(this).serialize();
        // Realizar la solicitud AJAX para actualizar el usuario
        $.ajax({
            url: '/admin_dashboard/edit_user/' + userId + '/',
            method: 'POST',
            data: formData,
            success: function(data) {
                if (data.success) {
                    location.reload(); // Recargar la página si la actualización es exitosa
                }
            }
        });
    });

    $('.delete-user').on('click', function() {
        var userId = $(this).data('id');
        // Realizar la solicitud AJAX para eliminar el usuario
        $.ajax({
            url: '/admin_dashboard/delete_user/' + userId + '/',
            method: 'POST',
            success: function(data) {
                if (data.success) {
                    location.reload(); // Recargar la página si la eliminación es exitosa
                }
            }
        });
    });
});
