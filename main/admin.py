from django.contrib import admin
from .models import Service, Carrito

# Registrar los modelos en el sitio de administración de Django
admin.site.register(Service)
admin.site.register(Carrito)
