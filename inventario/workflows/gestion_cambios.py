# solicitudes/workflows/gestion_cambios.py
from spiffworkflow.bpmn.parser.BpmnParser import BpmnParser
from spiffworkflow.workflow import Workflow

# Cargar BPMN y obtener el spec
parser = BpmnParser()
parser.add_bpmn_file('solicitudes/workflows/cambio_grupo.bpmn')
spec = parser.get_spec('CambioDeGrupo')  # ID del proceso en tu BPMN

def iniciar_solicitud(student_id, asignatura_id):
    workflow = Workflow(spec)
    workflow.set_data({
        'student_id': student_id,
        'asignatura_id': asignatura_id,
        'aprobado_profesor': None,
        'aprobado_coordinador': None,
    })
    workflow.start()
    return workflow