from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from datetime import date

User = get_user_model()

class BaseCaso(models.Model):
    REPRESENTANTE_CHOICES = [
        ('Demandante', 'Demandante'),
        ('Demandado', 'Demandado'),
        ('Martillero', 'Martillero'),
    ]

    demandante = models.CharField(max_length=255)
    demandado = models.CharField(max_length=255)
    sede = models.CharField(max_length=100, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    representante = models.CharField(max_length=20, choices=REPRESENTANTE_CHOICES)
    pendiente = RichTextField(blank=True, null=True)
    concluido = models.BooleanField(default=True, help_text="True => Activo, False => Concluido")

    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 2}, 
        verbose_name='Responsable (Área Legal)'
    )

    class Meta:
        abstract = True

    def alerta_color(self):
        hoy = date.today()
        
        if hasattr(self, 'seguimientos'):
            manager = self.seguimientos
        elif hasattr(self, 'seguimientos_penal'):
            manager = self.seguimientos_penal
        else:
            return "secondary"

        proximo_seguimiento = (
            manager
            .filter(fecha_alerta__gte=hoy)
            .order_by('fecha_alerta') 
            .first()
        )

        if not proximo_seguimiento:
            return "secondary" 

        dias_restantes = (proximo_seguimiento.fecha_alerta - hoy).days

        if dias_restantes <= 5:
            return "danger"     
        elif dias_restantes <= 15:
            return "warning"    
        else:
            return "success"    


class BaseSeguimiento(models.Model):
    ESTADO_CHOICES = [
        ('En proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
        ('Presentado', 'Presentado'),
        ('Notificado', 'Notificado'),
        ('Otros', 'Otros'),
    ]

    resolucion = models.CharField(max_length=255, blank=True, null=True)
    fecha_seguimiento = models.DateField(blank=True, null=True)
    seguimiento = RichTextField(null=True, blank=True)
    fecha_pendiente = models.DateField(blank=True, null=True) 
    pendiente = RichTextField(null=True, blank=True)
    responsable = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En proceso') 
    pdf = models.FileField(upload_to='seguimiento/', max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    editor = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_alerta = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseGasto(models.Model):
    fecha = models.DateField()
    detalle = models.CharField(max_length=255, blank=True, null=True)
    sustento = models.TextField(blank=True)
    pdf = models.FileField(upload_to='gastos_expediente/', max_length=255, blank=True, null=True)
    codigo_pago = models.CharField(max_length=255, blank=True, null=True)
    gastos_soles = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gastos_dolares = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    editor = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class CasoJudicial(BaseCaso):
    codigo = models.CharField(max_length=100, blank=True, null=True)
    fecha_compromiso = models.DateField(blank=True, null=True)
    expediente = models.CharField(max_length=100)
    materia = models.CharField(max_length=255, blank=True, null=True)
    juzgado = models.CharField(max_length=255, blank=True, null=True)
    
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 2},
        related_name='casos_asignados',
        verbose_name='Responsable (Área Legal)'
    )

    def __str__(self):
        return f"{self.expediente}"


class Seguimiento(BaseSeguimiento):
    caso = models.ForeignKey(CasoJudicial, on_delete=models.CASCADE, related_name='seguimientos')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='seguimientos_creados')
    estado = models.CharField(max_length=20, choices=BaseSeguimiento.ESTADO_CHOICES, default='Finalizado')

    def __str__(self):
        return f"Seguimiento - {self.caso.expediente} - {self.fecha_seguimiento}"


class Gasto(BaseGasto):
    seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE, related_name='gastos')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto - {self.seguimiento.caso.expediente} - {self.fecha}"


class CarpetaFiscal(BaseCaso):
    item = models.CharField(max_length=100, blank=True, null=True)
    carpeta_fiscal = models.CharField(max_length=100, blank=True, null=True)
    delito = models.CharField(max_length=100, blank=True, null=True)
    fiscalia = models.CharField(max_length=100, blank=True, null=True)

    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 2},
        related_name='casos_asignados_carpeta_fiscal',
        verbose_name='Responsable (Área Legal)'
    )

    def __str__(self):
        return f"{self.carpeta_fiscal}"


class SeguimientoFiscal(BaseSeguimiento):
    caso = models.ForeignKey(CarpetaFiscal, on_delete=models.CASCADE, related_name='seguimientos_penal')
    inter = models.BooleanField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='seguimientos_creados_fiscal')
    
    estado = models.CharField(max_length=20, choices=BaseSeguimiento.ESTADO_CHOICES, default='En proceso')

    def __str__(self):
        return f"Seguimiento - {self.caso.carpeta_fiscal} - {self.fecha_seguimiento}"


class GastoFiscal(BaseGasto):
    seguimiento = models.ForeignKey(SeguimientoFiscal, on_delete=models.CASCADE, related_name='gastos_fiscal')

    def __str__(self):
        return f"Gasto - {self.seguimiento.caso.carpeta_fiscal} - {self.fecha} - S/ {self.gastos_soles}"
 
class RegistroActividad(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    actividad = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='registro_user')

    def __str__(self):
        return f"{self.nombre} - {self.actividad}"