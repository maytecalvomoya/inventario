from SpiffWorkflow.camunda.parser.CamundaParser import CamundaParser
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.task import TaskState
import pickle

def load_workflow(bpmn_path: str, process_id: str) -> BpmnWorkflow:
    """Carga un BPMN y devuelve el workflow listo para ejecutar."""
    parser = CamundaParser()
    parser.add_bpmn_file(bpmn_path)
    spec = parser.get_spec(process_id)

    workflow = BpmnWorkflow(spec)
    workflow.data = {}  # Diccionario global de variables
    workflow.do_engine_steps()  # Avanza tareas automáticas iniciales

    return workflow

def serialize_workflow(workflow: BpmnWorkflow) -> bytes:
    """Convierte un workflow en bytes para guardar en la base de datos."""
    return pickle.dumps(workflow)

def deserialize_workflow(workflow_bytes: bytes) -> BpmnWorkflow:
    """Recupera un workflow desde los bytes almacenados en la base de datos."""
    return pickle.loads(workflow_bytes)

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
            workflow.data.update(data)
            task.data.update(data)

        task.complete()
        workflow.do_engine_steps()
        print(f"Tarea {task.task_spec.name} completada.")
    else:
        print(f"No se puede completar la tarea {task.task_spec.name}. "
              f"Estado: {task.state}, ¿Manual?: {task.task_spec.manual}")














