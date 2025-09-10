from django.urls import path
from . import views
# from .views import crear_solicitud

'''
urlpatterns = [
    path('nueva_solicitud/', crear_solicitud, name='crear_solicitud'),
    #path('ajax/load-titulaciones/', views.load_titulaciones, name='ajax_load_titulaciones'),
]
'''

urlpatterns = [
    # Estudiantes
    path('solicitudes/nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('solicitudes/mis_solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),

    # Coordinadores
    path('coordinador/pendientes/', views.solicitudes_pendientes, name='solicitudes_pendientes'),
    path('coordinador/completar/<int:solicitud_id>/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
]
