from rest_framework.exceptions import ValidationError

from .models import Task, StatusChoice

from user.models import User




"""Hecho con IA -> me parecio interesante implementar este diccionario para hacer las validaciones más simples"""
VALID_TRANSITIONS = {
    StatusChoice.TODO:        [StatusChoice.IN_PROGRESS],
    StatusChoice.IN_PROGRESS: [StatusChoice.DONE],
    StatusChoice.DONE:        [],
}


# Recibo todos los campos como opcionales menos 'tittle'
def create_task(title, description=None, assigned_to_id=None):
    if assigned_to_id:
        if not User.objects.filter(id=assigned_to_id).exists():
            raise ValidationError({"assigned_to": "El usuario no existe"})
    
    return Task.objects.create(
        title=title,
        description=description,
        assigned_to_id=assigned_to_id
    )
    

def update_status(task_id, new_status):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise ValidationError({"task": "La tarea no existe"})
    
    if new_status not in VALID_TRANSITIONS[task.status]:
        raise ValidationError({
            "status": f"Este salto de estado no es permitido: de {task.status} a {new_status}"
        })
    
    task.status = new_status
    task.save()
    return task


"""Hecho con IA"""
def assign_task(task_id, user_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise ValidationError({"task": "La tarea no existe"})
    
    if user_id is not None and not User.objects.filter(id=user_id).exists():
        raise ValidationError({"assigned_to": "El usuario no existe"})
    
    task.assigned_to_id = user_id
    task.save()
    return task


"""Hecho con IA"""
def list_tasks(status=None, assigned_name=None):
    qs = Task.objects.select_related('assigned_to')
    
    if status:
        qs = qs.filter(status=status)
    
    if assigned_name:
        qs = qs.filter(assigned_to__first_name__icontains=assigned_name)
    
    return qs
