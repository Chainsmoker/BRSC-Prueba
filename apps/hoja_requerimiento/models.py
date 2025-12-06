from django.db import models

class Anios(models.Model):
    anio = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.anio

class Q1_T1(models.Model):
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento")
    proveedor = models.CharField(max_length=255, verbose_name="Proveedor")
    concepto = models.TextField(verbose_name="Concepto")
    soles = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto en Soles")
    dolares = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto en Dólares")
    quincena = models.BooleanField(default=False)
    anio = models.ForeignKey(
        Anios,
        on_delete=models.CASCADE,
        related_name='gastos',
        verbose_name="Año"
    )

    def __str__(self):
        return f"{self.proveedor} - {self.concepto[:30]}..."