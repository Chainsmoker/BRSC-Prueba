from django.urls import path, include
from .views import AsistenciaView

app_name = 'asistencia'

urlpatterns = [
    path("", AsistenciaView.as_view(), name="home"), 
]
