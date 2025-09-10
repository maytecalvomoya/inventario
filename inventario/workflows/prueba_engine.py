import sys

# Añadir la raíz del proyecto al sys.path
sys.path.append('/home/Mayte/gsolcam')

from inventario.workflows.engine import load_workflow, get_ready_user_tasks, complete_user_task

# Ruta al BPMN y ID del proceso
bpmn_path = "/home/Mayte/gsolcam/inventario/workflows/bpmn/diagram_1.bpmn"
process_id = "Process_0flhbkn"

# Cargar el workflow
workflow = load_workflow(bpmn_path, process_id)

# Inicializar variable que tu BPMN necesita
workflow.data["cumple_criterios"] = True

# Loop para completar todas las tareas de usuario
while True:
    ready_tasks = get_ready_user_tasks(workflow)
    if not ready_tasks:
        print("No hay más tareas listas.")
        break
    for task in ready_tasks:
        print(f"Tarea lista: {task.task_spec.name} (id: {task.id})")

        # Completa la tarea pasando explícitamente la variable
        complete_user_task(workflow, task.id, {"cumple_criterios": workflow.data["cumple_criterios"]})
