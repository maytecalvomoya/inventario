from django import forms
from .models import Solicitud

#Formulario para que el estudiante pueda cumplimentar los datos de la solicitud
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['facultad', 'titulacion', 'asignatura', 'grupo', 'grupo_deseado', 'turno', 'turno_deseado']

'''
#Formulario para que el coordinador pueda aprobar o rechazar la solicitud
class GestionForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['estado','observaciones']
'''