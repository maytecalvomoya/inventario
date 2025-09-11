#import os
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SolicitudForm
from .workflows.engine import load_workflow, get_ready_user_tasks, complete_user_task
from .workflows.engine import serialize_workflow, deserialize_workflow
#from utilidades.mail import enviar_correo
import base64
from .models import Solicitud
from django.contrib import messages
#from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
from .forms import LoginForm

ruta_bpmn = "/home/Mayte/gsolcam/inventario/workflows/bpmn/diagram_1.bpmn"
id_proceso = "Process_0flhbkn"


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)  # pasa request al form
        if form.is_valid():
            user = form.get_user()  # obtiene el usuario autenticado
            login(request, user)     # inicia sesión
            return redirect('crear_solicitud')  # redirige tras login
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

@login_required
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
            return redirect('mis_solicitudes')
    else:
        form = SolicitudForm()
    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})

@login_required
def mis_solicitudes(request):
    # Obtiene las solicitudes del usuario que se haya logueado previamente
    solicitudes = Solicitud.objects.filter(estudiante=request.user).order_by('-fecha_solicitud')

    return render(request, 'solicitudes/mis_solicitudes.html', {
        'solicitudes': solicitudes
    })


# ----------------------------
# Decorador para coordinadores
# ----------------------------
def es_coordinador(user):
    return user.is_authenticated and user.groups.filter(name="Coordinadores").exists()

def requiere_ser_coordinador(view_func):
    @wraps(view_func)
    @login_required
    @user_passes_test(es_coordinador)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

#Función que obtiene las solicitudes pendientes para el coordinador
@requiere_ser_coordinador
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

    return render(request, 'inventario/pendientes.html', {
        'solicitudes_con_tareas': solicitudes_con_tareas
    })

#Función para completar las tareas por parte del coordinador
@requiere_ser_coordinador
def completar_tarea(request, solicitud_id, tarea_id):
    # Recupera la solicitud
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    # Valido que la solicitud tenga workflow
    if not solicitud.workflow_json:
        messages.error(request, "Error: esta solicitud no tiene workflow asociado.")
        return redirect('solicitudes_pendientes')

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
        #if workflow.is_done():
        #    solicitud.estado = 'aprobado' if aprobado else 'rechazado'
        if not get_ready_user_tasks(workflow):
            solicitud.estado = 'aprobado' if aprobado else 'rechazado'



        solicitud.save()

        # Mensaje de éxito para mostrar en la misma página
        messages.success(
            request,
            f"Tarea '{tarea_id}' de la solicitud de {solicitud.estudiante.get_full_name() or solicitud.estudiante.username} completada."
        )

    # Siempre redirige a la página de pendientes (inline)
    return redirect('solicitudes_pendientes')









