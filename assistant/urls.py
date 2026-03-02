from django.urls import path
from .views import consult_assistan




urlpatterns = [
    path('consult/', consult_assistan, name='consult_assistant')
]
