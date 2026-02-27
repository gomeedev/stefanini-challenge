from django.db import models
from user.models import User




class StatusChoice(models.TextChoices):
    TODO        = 'TODO', 'Por hacer'
    IN_PROGRESS = 'IN_PROGRESS', 'En progreso'
    DONE        = 'DONE', 'Terminado'

class Task(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    status      = models.CharField(max_length=12, choices=StatusChoice.choices, default=StatusChoice.TODO)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    class Meta:
        db_table = 'task'
        ordering = ['-created']
        