from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Service, Carrito, CarritoItem, DiscountCode, Purchase, ContactMessage
from .forms import UserRegistrationForm, ProfileRegistrationForm, ProfileForm, UserForm, ServiceForm, ContactForm, CartItemForm, CarritoForm, DiscountCodeForm, EditUserForm
from django.contrib.auth import logout
import os
from django.db import transaction, IntegrityError
from django.conf import settings

# Función para verificar si el usuario es administrador
def is_admin(user):
    return user.is_superuser

# Definir la vista de la página de inicio
def home(request):
    services = Service.objects.all()
    latest_services = Service.objects.order_by('-created_at')[:3]  # Obtener los últimos 3 servicios
    latest_service = Service.objects.order_by('-created_at').first() # Obtener el ultimo servicio
    return render(request, 'home.html', {
        'services': services,
        'latest_services': latest_services,
        'latest_service' : latest_service
    })

# Definir la vista de la página de servicios
def services(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.profile.role == 'mecanico':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.image = 'images/' + form.cleaned_data['custom_image']
            service.save()
            return JsonResponse({
                'success': True,
                'service': {
                    'id': service.id,
                    'title': service.title,
                    'description': service.description,
                    'price': str(service.price),
                    'image': service.image
                }
            })
    else:
        form = ServiceForm()

    services = Service.objects.all()
    return render(request, 'services.html', {'form': form, 'services': services})

# Definir la vista para eliminar un servicio
def delete_service(request, service_id):
    if request.method == 'POST' and request.user.is_authenticated and request.user.profile.role == 'mecanico':
        try:
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            return JsonResponse({'success': True})
        except Service.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Unauthorized request'})

# Verificar si el usuario es administrador
def admin_check(user):
    return user.is_staff

# Vista para el dashboard de administrador
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    discount_codes = DiscountCode.objects.all()
    purchases = Purchase.objects.order_by('-created_at')[:5]  # Las últimas 5 compras
    contact_messages = ContactMessage.objects.all()  # Obtener todos los mensajes de contacto
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'discount_codes': discount_codes,
        'purchases': purchases,
        'contact_messages': contact_messages
    })

@user_passes_test(is_admin)
def view_contact_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'view_contact_message.html', {'message': message})


@user_passes_test(is_admin)
def delete_contact_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    return redirect('admin_dashboard')

# Vista para agregar un código de descuento
@user_passes_test(is_admin)
def add_discount_code(request):
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = DiscountCodeForm()
    return render(request, 'add_discount_code.html', {'form': form})

# Vista para editar un usuario
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

# Vista para eliminar un usuario
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_user.html', {'user': user})

# Vista para editar un código de descuento
@user_passes_test(is_admin)
def edit_discount_code(request, code_id):
    code = get_object_or_404(DiscountCode, id=code_id)
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = DiscountCodeForm(instance=code)
    return render(request, 'edit_discount_code.html', {'form': form})

# Vista para eliminar un código de descuento
@user_passes_test(is_admin)
def delete_discount_code(request, code_id):
    code = get_object_or_404(DiscountCode, id=code_id)
    if request.method == 'POST':
        code.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_discount_code.html', {'code': code})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')

# Vista para la página 'sobre'
def sobre(request):
    services = Service.objects.all()
    latest_services = Service.objects.order_by('-created_at')[:3]  # Obtener los últimos 3 servicios

    return render(request, 'sobre.html', {
        'services': services,
        'latest_services': latest_services
    })

# Vista para la página de contacto
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the message to the database
            form.save()
            messages.success(request, "Tu mensaje ha sido enviado y almacenado correctamente.")
            return redirect('contact_success')
        else:
            messages.error(request, "Por favor corrige los errores a continuación.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# Vista para la página de éxito de contacto
def contact_success(request):
    return render(request, 'contact_success.html')

# Vista para la página de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Nombre de usuario o contraseña no válidos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña no válidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para la página de registro
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.save()
                    
                    if not Profile.objects.filter(user=user).exists():
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.save()
                    
                    messages.success(request, "Registro exitoso. Por favor inicia sesión.")
                    return redirect('login')
            except IntegrityError as e:
                if user.pk:
                    user.delete()
                messages.error(request, f"Ocurrió un error al crear el perfil: {str(e)}. Inténtalo de nuevo.")
        else:
            messages.error(request, "Por favor corrija los errores a continuación.")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

# Vista para la página de perfil
@login_required
def profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    purchases = Purchase.objects.filter(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'purchases': purchases})

# Vista para ver el carrito de compras
@login_required
def view_cart(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_items = CarritoItem.objects.filter(carrito=carrito)

    if request.method == 'POST':
        form = CartItemForm(request.POST, usuario=request.user)
        if form.is_valid():
            servicio = form.cleaned_data['servicio']
            cantidad = form.cleaned_data['cantidad']
            discount_code = form.cleaned_data['discount_code']
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, servicio=servicio)
            carrito_item.cantidad = cantidad
            if discount_code:
                try:
                    discount = DiscountCode.objects.get(code=discount_code, is_active=True)
                    carrito_item.descuento = discount.discount  # Aplicar descuento como porcentaje
                except DiscountCode.DoesNotExist:
                    messages.error(request, "Código de descuento no válido o expirado.")
                    return redirect('cart')
            carrito_item.save()
            messages.success(request, "Carrito actualizado correctamente.")
            return redirect('cart')

    else:
        form = CartItemForm(usuario=request.user)

    total_price = sum(item.total_price() for item in carrito_items)
    
    return render(request, 'cart.html', {'carrito_items': carrito_items, 'total_price': total_price, 'form': form})

# Vista para eliminar un ítem del carrito
def delete_cart_item(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    item.delete()
    return redirect('cart')

# Vista para añadir un servicio al carrito
def add_to_cart(request, service_id):
    if request.user.is_authenticated:
        service = get_object_or_404(Service, id=service_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, servicio=service)
        if created:
            carrito_item.cantidad = 1  # Añadir uno por defecto si es un nuevo ítem
        else:
            carrito_item.cantidad += 1  # Incrementar la cantidad si el ítem ya existe
        carrito_item.save()
        return redirect('cart')
    else:
        return redirect('login')

# Vista para aplicar descuento en el carrito
def apply_discount(request):
    if request.method == 'POST':
        code = request.POST.get('discount_code')
        try:
            discount = DiscountCode.objects.get(code=code)
            request.session['discount'] = discount.discount
            return redirect('cart')
        except DiscountCode.DoesNotExist:
            request.session['discount'] = 0.0
            return redirect('cart')

# Vista para la página de checkout
def checkout(request):
    if request.method == 'POST':
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_items = CarritoItem.objects.filter(carrito=carrito)
        
        # Guardar la compra en el historial del usuario
        for item in carrito_items:
            Purchase.objects.create(
                user=request.user,
                service=item.servicio,
                cantidad=item.cantidad,
                descuento=item.descuento,
                total_price=item.total_price()
            )
        
        # Limpiar el carrito
        carrito_items.delete()
        
        return redirect('checkout_success')
    
    return render(request, 'checkout.html')

# Vista para la página de éxito de checkout
def checkout_success(request):
    return render(request, 'checkout_success.html')
