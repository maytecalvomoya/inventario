from django.db import models
from django.contrib.auth.models import User

class Facultad(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)

    #Hago esto para indicar a Django qué debe mostrar en los formularios
    def __str__(self):
        return self.nombre

class Titulacion(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    #cod_facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT, default='Facultad de Ciencias')
    titulacion = models.ForeignKey(Titulacion, on_delete=models.PROTECT)
    asignatura = models.CharField(max_length=100)
    grupo = models.CharField(max_length=10)
    turno = models.CharField(max_length=10)
    grupo_deseado = models.CharField(max_length=10, default='Grupo 1')
    turno_deseado = models.CharField(max_length=10, default='Tarde')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.CharField(max_length=400, default='--')
    workflow_json = models.TextField(blank=True, null=True)  # Aquí guardamos el estado del workflow
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

