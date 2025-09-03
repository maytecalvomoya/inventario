from django.shortcuts import render, redirect
from .forms import SolicitudForm
#from django.http import JsonResponse
#from .models import Titulacion

'''
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.estudiante = request.user
            solicitud.save()
            return redirect('exito')
    else:
        form = SolicitudForm()
    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})
'''

def crear_solicitud(request):
    facultad_id = None

    if request.method == 'POST':
        facultad_id = request.POST.get('facultad')
        form = SolicitudForm(request.POST, facultad_id=facultad_id)
        if form.is_valid():
            form.save()
            return redirect('crear_solicitud')
    else:
        form = SolicitudForm()

    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})





