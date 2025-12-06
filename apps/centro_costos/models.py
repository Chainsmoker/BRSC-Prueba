from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class CentroDeCostos(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class TipoDeGasto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Actividad(models.Model):
    TIPO = [
        ('Por separado', 'Por separado'),
        ('A todo costo', 'A todo costo'),
    ]

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    centro_de_costos = models.ForeignKey(CentroDeCostos, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO)
    responsable = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class GastoTA2020(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    fecha = models.DateField()
    detalle = models.TextField()
    documento = models.CharField(max_length=100, blank=True, null=True)
    debe = models.DecimalField(max_digits=10, decimal_places=2)
    haber = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_gasto = models.ForeignKey(TipoDeGasto, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.detalle

class CantaCallao(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    detalle = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(100)])
    referencia = models.CharField(max_length=100, blank=True, null=True)
    monto1 =  models.CharField(max_length=10, blank=True, null=True)
    monto2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.detalle[:30]}"

class NuevoGasto(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre or "Nuevo Gasto"

class Gasto(models.Model):
    origen = models.ForeignKey(NuevoGasto, on_delete=models.CASCADE, related_name='gastos')
    codigo = models.CharField(max_length=100, unique=True, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    referencia = models.CharField(max_length=255, blank=True, null=True)
    pdf = models.FileField(upload_to='gastos', blank=True, null=True, max_length=255)
    monto_soles = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    monto_dolares = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actividad = models.CharField(max_length=255, blank=True, null=True)
    tipo_gasto = models.CharField(max_length=100, blank=True, null=True)
    es_ingreso = models.BooleanField(default=False)

    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ultima_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    editor = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.detalle[:50]}" if self.codigo and self.detalle else "Gasto General"

class GastoN9(models.Model):
    expediente = models.CharField(max_length=100, blank=True, null=True)
    juzgado = models.CharField(max_length=100, blank=True, null=True)
    demandante = models.CharField(max_length=100, blank=True, null=True)
    demandado = models.CharField(max_length=100, blank=True, null=True)
    materia = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    escrito = models.TextField(blank=True, null=True)
    concepto = models.CharField(max_length=255, blank=True, null=True)
    monto_soles = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    monto_dolares = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    pdf = models.FileField(upload_to='gastos', blank=True, null=True, max_length=255)

    def __str__(self):
        return f"{self.expediente}"