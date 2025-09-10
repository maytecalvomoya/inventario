from django.urls import path
#from . import views
from .views import crear_solicitud

urlpatterns = [
    path('nueva_solicitud/', crear_solicitud, name='crear_solicitud'),
    #path('ajax/load-titulaciones/', views.load_titulaciones, name='ajax_load_titulaciones'),
]


