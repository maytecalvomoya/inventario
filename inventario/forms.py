from django import forms
from .models import Solicitud, Titulacion

'''
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['facultad', 'titulacion', 'asignatura', 'grupo', 'turno']
'''

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['facultad', 'titulacion', 'asignatura', 'grupo', 'turno']

    def __init__(self, *args, **kwargs):
        facultad_id = kwargs.pop('facultad_id', None)
        super().__init__(*args, **kwargs)

        if facultad_id:
            self.fields['titulacion'].queryset = Titulacion.objects.filter(cod_facultad_id=facultad_id)
        else:
            self.fields['titulacion'].queryset = Titulacion.objects.none()
