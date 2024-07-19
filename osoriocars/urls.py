from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static


#Configuración de urls mediante vistas para que cada página sea visible
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.view_cart, name='cart'),
    path('sobre/', views.sobre, name='sobre'),
    path('add_to_cart/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/apply_discount/', views.apply_discount, name='apply_discount'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin_dashboard/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_dashboard/add_discount_code/', views.add_discount_code, name='add_discount_code'),
    path('admin_dashboard/edit_discount_code/<int:code_id>/', views.edit_discount_code, name='edit_discount_code'),
    path('admin_dashboard/delete_discount_code/<int:code_id>/', views.delete_discount_code, name='delete_discount_code'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
