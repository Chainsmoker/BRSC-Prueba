from django.db import models

class Partida(models.Model):
    codigo = models.CharField(max_length=10, blank=True, null=True)
    partida = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    pg = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    costo = models.CharField(max_length=100, blank=True, null=True)
    centro_costos = models.CharField(max_length=100, blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    pdf = models.FileField(upload_to='partidas', blank=True, null=True, max_length=255)


class Plano(models.Model):
    partida = models.CharField(max_length=100,blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    pg = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    costo = models.CharField(max_length=100, blank=True, null=True)
    centro_costos = models.CharField(max_length=100,blank=True, null=True)
    pdf = models.FileField(upload_to='planos_y_otros', blank=True, null=True, max_length=255)



