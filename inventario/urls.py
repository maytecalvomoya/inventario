from django.urls import path
from . import views

urlpatterns = [
    # Estudiantes
    path('solicitudes/nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('solicitudes/mis_solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),

    # Coordinadores
    path('coordinador/pendientes/', views.solicitudes_pendientes, name='solicitudes_pendientes'),
    path('coordinador/completar/<int:solicitud_id>/<uuid:tarea_id>/', views.completar_tarea, name='completar_tarea')
]





