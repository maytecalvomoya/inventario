from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth import views
#from django.contrib.auth impor auth_views
from inventario.views import login_view #Importa el login personalizado
#from inventario.forms import LoginForm
from django.contrib.auth.views import LogoutView
#from gsolcam.inventario.views import redireccion_despues_login
from inventario.views import redireccion_despues_login


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('redireccion/', redireccion_despues_login, name='redireccion'),

    path('', include('inventario.urls')),
]
