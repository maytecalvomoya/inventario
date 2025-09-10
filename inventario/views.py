#import os
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SolicitudForm
from .workflows.engine import load_workflow, get_ready_user_tasks, complete_user_task
from .workflows.engine import serialize_workflow, deserialize_workflow
#from utilidades.mail import enviar_correo
import base64
from .models import Solicitud
from django.contrib import messages

ruta_bpmn = "/home/Mayte/gsolcam/inventario/workflows/bpmn/diagram_1.bpmn"
id_proceso = "Process_0flhbkn"

def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.estudiante = request.user

            # Cargar workflow
            workflow = load_workflow(ruta_bpmn, id_proceso)

            # Serializar workflow a bytes y luego a base64 para guardar en TextField
            workflow_bytes = serialize_workflow(workflow)
            solicitud.workflow_json = base64.b64encode(workflow_bytes).decode('utf-8')

            solicitud.save()
            return redirect('crear_solicitud')
    else:
        form = SolicitudForm()
    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})

#Función que obtiene las solicitudes pendientes para el coordinador
def solicitudes_pendientes(request):
    solicitudes = Solicitud.objects.filter(estado='pendiente')

    solicitudes_con_tareas = []
    for solicitud in solicitudes:
        # Recupera workflow desde base64
        workflow_bytes = base64.b64decode(solicitud.workflow_json)
        workflow = deserialize_workflow(workflow_bytes)

        # Obtiene tareas listas para el usuario
        tareas = get_ready_user_tasks(workflow)

        solicitudes_con_tareas.append({
            'solicitud': solicitud,
            'tareas': tareas
        })

    return render(request, 'solicitudes/pendientes.html', {
        'solicitudes_con_tareas': solicitudes_con_tareas
    })

#Función para completar las tareas por parte del coordinador
def completar_tarea(request, solicitud_id, tarea_id):
    # Recupera la solicitud
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    # Recupera el workflow desde base64
    workflow_bytes = base64.b64decode(solicitud.workflow_json)
    workflow = deserialize_workflow(workflow_bytes)

    if request.method == 'POST':
        # Obtiene la decisión del coordinador
        aprobado = request.POST.get('aprobado') == 'true'
        observaciones = request.POST.get('observaciones', '--')
        solicitud.observaciones = observaciones

        try:
            complete_user_task(workflow, tarea_id, {'aprobado': aprobado})
        except Exception as e:
            messages.error(request, f'Error al completar la tarea: {e}')
            return redirect('solicitudes_pendientes')

        # Guarda el workflow actualizado en la base de datos (base64)
        solicitud.workflow_json = base64.b64encode(serialize_workflow(workflow)).decode('utf-8')

        # Actualiza el estado final si el workflow terminó
        #if workflow.is_complete():
        #    solicitud.estado = 'aprobado' if workflow.data.get('aprobado_coordinador', False) else 'rechazado'

        if workflow.is_complete():
            solicitud.estado = 'aprobado' if aprobado else 'rechazado'


        solicitud.save()
        #estado_texto = "aprobada" if solicitud.estado == "aprobado" else "rechazada"

        #Se envía email al estudiante
        #enviar_correo("mayte.calvo.moya@gmail.com", "Este es el asunto", "Este es el cuerpo del mensaje")

        return redirect('solicitudes_pendientes')

    # Mostrar confirmación antes de completar
    tarea = next(t for t in get_ready_user_tasks(workflow) if t.id == tarea_id)
    return render(request, 'inventario/completar_tarea.html', {
        'solicitud': solicitud,
        'tarea': tarea
    })






