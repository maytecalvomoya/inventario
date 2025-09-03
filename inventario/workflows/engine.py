from SpiffWorkflow.camunda.parser.CamundaParser import CamundaParser
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.task import TaskState

ruta_bpmn = "/home/Mayte/gsolcam/inventario/workflows/bpmn/diagram_1.bpmn"
id_proceso = "Process_0flhbkn"

def load_workflow(bpmn_path: str, process_id: str) -> BpmnWorkflow:
    """Carga un BPMN y devuelve el workflow listo para ejecutar."""
    parser = CamundaParser()
    parser.add_bpmn_file(bpmn_path)
    spec = parser.get_spec(process_id)

    workflow = BpmnWorkflow(spec)
    workflow.data = {}  # Diccionario global de variables
    workflow.do_engine_steps()  # Avanza tareas automáticas iniciales

    return workflow


def get_ready_user_tasks(workflow: BpmnWorkflow):
    """Devuelve la lista de tareas de usuario que están listas para completar."""
    return [
        task for task in workflow.get_tasks()
        if task.state == TaskState.READY and task.task_spec.manual
    ]


def complete_user_task(workflow: BpmnWorkflow, task_id: str, data: dict | None = None):
    """Completa una tarea de usuario con datos opcionales."""
    task = workflow.get_task_from_id(task_id)
    if task.state == TaskState.READY and task.task_spec.manual:
        if data:
            # Actualiza variables globales y locales de la tarea
            workflow.data.update(data)
            task.data.update(data)

        task.complete()
        workflow.do_engine_steps()
        print(f"Tarea {task.task_spec.name} completada.")
        #print("Workflow.data:", workflow.data)
        #print("Task.data:", task.data)
    else:
        print(f"No se puede completar la tarea {task.task_spec.name}. "
              f"Estado: {task.state}, ¿Manual?: {task.task_spec.manual}")














