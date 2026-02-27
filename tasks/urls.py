from django.urls import path
from .views import tasks_view, task_status_view, task_assign_view




urlpatterns = [
    path('', tasks_view, name='tasks'),
    path('<int:pk>/status/', task_status_view, name='task-status'),
    path('<int:pk>/assign/', task_assign_view, name='task-assign'),
]
