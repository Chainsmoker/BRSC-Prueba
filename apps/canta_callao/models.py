from django.db import models

# class Proyecto(models.Model):
#     proyecto = models.CharField(max_length=255)
#     presupuesto = models.DecimalField(max_digits=12, decimal_places=2)
#     sustento = models.FileField(upload_to='Proyecto_CantaCallao/', blank=True, null=True)
#     fecha = models.DateField()

#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Proyecto Canta Callao"
#         verbose_name_plural = "Proyectos Canta Callao"
#         ordering = ['-fecha_creacion']

#     def __str__(self):
#         return f"{self.proyecto}"


# class Actividad(models.Model):
#     proyecto = models.ForeignKey(
#         Proyecto,
#         on_delete=models.CASCADE,
#         related_name='actividades'
#     )
#     descripcion = models.CharField(max_length=255)
#     sustento = models.FileField(upload_to='Proyecto_CantaCallao/', blank=True, null=True)
#     fecha = models.DateField()

#     debe = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
#     haber = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
#     saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Actividad"
#         verbose_name_plural = "Actividades"
#         ordering = ['-fecha']

#     def __str__(self):
#         return f"{self.descripcion} - {self.fecha}"
