from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventario.views import login_view #Importa el login personalizado
from inventario.forms import LoginForm    # tu formulario con labels modificados

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('', include('inventario.urls')),
    path('solicitudes/login/', auth_views.LoginView.as_view(template_name='solicitudes/login.html'), name='login'),
    path('solicitudes/logout/', auth_views.LogoutView.as_view(next_page='/solicitudes/login/'), name='logout'),
]
'''


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Login personalizado opcional
    path('login/', login_view, name='login'),

    # Login que se usa para redirección de @login_required
    path(
        'solicitudes/login/',
        auth_views.LoginView.as_view(
            template_name='solicitudes/login.html',
            authentication_form=LoginForm  # <- usa tu LoginForm con "Usuario"
        ),
        name='login'
    ),

    # Logout
    path(
        'solicitudes/logout/',
        auth_views.LogoutView.as_view(next_page='/solicitudes/login/'),
        name='logout'
    ),

    # URLs de la app inventario
    path('', include('inventario.urls')),
]
