from django.db import models
from django.contrib.auth.models import User

# Modelo para el perfil del usuario
class Profile(models.Model):
    ROLE_CHOICES = [
        ('mecanico', 'Mecanico'),
        ('comprador', 'Comprador')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='comprador')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    rut = models.CharField(max_length=12, blank=True)

# Crear perfil de usuario al crear un usuario
def create_user_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)

# Modelo para los mensajes de contacto
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

# Modelo para los servicios
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='main/static/images/')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

# Modelo para las compras
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

# Modelo para los códigos de descuento
class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

# Modelo para el carrito de compras
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Service, through='CarritoItem')

# Modelo para los ítems en el carrito de compras
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Service, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    # Calcular el precio total del ítem teniendo en cuenta el descuento
    def total_price(self):
        total = self.servicio.price * self.cantidad
        discount_amount = total * (self.descuento / 100)
        total_after_discount = total - discount_amount
        return max(total_after_discount, 0)
