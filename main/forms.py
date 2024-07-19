from django import forms
from django.contrib.auth.models import User
from .models import Profile, Service, ContactMessage, CarritoItem, DiscountCode
import os
from django.conf import settings

# Formulario para editar un usuario
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'is_staff': 'Es administrador',
        }

# Formulario para un código de descuento
class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount', 'is_active']
        labels = {
            'code': 'Código',
            'discount': 'Descuento',
            'is_active': 'Está activo',
        }

# Formulario para un servicio
class ServiceForm(forms.ModelForm):
    custom_image = forms.ChoiceField(choices=[], label="Imagen")

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        # Obtener las imágenes disponibles en la carpeta de imágenes
        images_path = os.path.join(settings.BASE_DIR, 'main/static/images')
        images = [(img, img) for img in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, img))]
        self.fields['custom_image'].choices = images
        if 'image' in self.fields:
            del self.fields['image']

    class Meta:
        model = Service
        fields = ['title', 'description', 'price']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'price': 'Precio',
        }

# Formulario para un ítem en el carrito
class CartItemForm(forms.ModelForm):
    servicio = forms.ModelChoiceField(queryset=Service.objects.none(), label="Servicio en Carrito")
    discount_code = forms.CharField(max_length=50, required=False, label="Código de Descuento")

    class Meta:
        model = CarritoItem
        fields = ['servicio', 'cantidad', 'discount_code']
        labels = {
            'servicio': 'Servicio',
            'cantidad': 'Cantidad',
            'discount_code': 'Código de Descuento',
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(CartItemForm, self).__init__(*args, **kwargs)
        if usuario:
            carrito_items = CarritoItem.objects.filter(carrito__usuario=usuario)
            servicios = Service.objects.filter(id__in=carrito_items.values_list('servicio', flat=True))
            self.fields['servicio'].queryset = servicios
            self.fields['servicio'].label_from_instance = lambda obj: obj.title  # Mostrar el nombre del servicio

# Formulario para el carrito
class CarritoForm(forms.ModelForm):
    servicio = forms.ModelChoiceField(queryset=Service.objects.all(), label="Servicio")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")
    codigo_descuento = forms.CharField(required=False, label="Código de Descuento")

    class Meta:
        model = CarritoItem
        fields = ['servicio', 'cantidad', 'codigo_descuento']
        labels = {
            'servicio': 'Servicio',
            'cantidad': 'Cantidad',
            'codigo_descuento': 'Código de Descuento',
        }

# Formulario para el formulario de contacto
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Nombre',
            'email': 'Correo electrónico',
            'subject': 'Asunto',
            'message': 'Mensaje',
        }

# Formulario para los datos de usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }

# Formulario para el perfil del usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'rut', 'role']
        labels = {
            'phone_number': 'Número de teléfono',
            'address': 'Dirección',
            'rut': 'RUT',
            'role': 'Rol',
        }

# Formulario para registrar un nuevo usuario
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

# Formulario para registrar el perfil del usuario
class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'rut', 'role']
        labels = {
            'phone_number': 'Número de teléfono',
            'address': 'Dirección',
            'rut': 'RUT',
            'role': 'Rol',
        }
