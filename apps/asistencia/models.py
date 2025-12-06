from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Asistencia(models.Model):
    trabajador = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    entrada = models.TimeField(null=True, blank=True)
    salida = models.TimeField(null=True, blank=True)
    horas_trabajadas = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Asistencia de {self.trabajador.username} - {self.fecha}"
