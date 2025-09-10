from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
    path('solicitudes/login/', auth_views.LoginView.as_view(template_name='solicitudes/login.html'), name='login'),
    path('solicitudes/logout/', auth_views.LogoutView.as_view(next_page='/solicitudes/login/'), name='logout'),
]



