from datetime import date

from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField
from tinymce.models import HTMLField

User = get_user_model()

class Tramite(models.Model):
    kardex = models.CharField(max_length=15, unique=True, blank=True, null=True, editable=False) # 
    fecha = models.DateField(blank=True, null=True)
    ult_revision = models.DateField(blank=True, null=True)
    destinatario = models.CharField(max_length=100, blank=True, null=True)
    partes_intervinientes = models.CharField(max_length=100, blank=True, null=True)
    sumilla = HTMLField(null=True, blank=True)
    tramite_tipo = models.CharField(max_length=100, blank=True, null=False)
    pendiente = HTMLField(null=True, blank=True)
    concluido = models.BooleanField(default=True, help_text="True => Activo, False => Concluido")

    responsable2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=~Q(username='user8'),
        related_name='casos_asignados_tramite',
        verbose_name='Responsable (Área Legal)'
    )

    def __str__(self):
        return f"{self.kardex} - {self.tramite_tipo}"
    
    def alerta_color(self):
        hoy = date.today()

        proximo_seguimiento = (
            self.seguimientos_tramites
            .filter(fecha_alerta__gte=hoy)
            .order_by('fecha_alerta')
            .first()
        )

        if not proximo_seguimiento:
            return "secondary"

        dias_restantes = (proximo_seguimiento.fecha_alerta - hoy).days

        if dias_restantes <= 5:
            return "danger"
        elif dias_restantes <= 10:
            return "warning"
        else:
            return "success"

    def save(self, *args, **kwargs):
        if self._state.adding and not self.kardex:
            last_tramite = Tramite.objects.filter(kardex__isnull=False).order_by('-id').first()

            if last_tramite and last_tramite.kardex and last_tramite.kardex.startswith('T'):
                try:
                    last_number = int(last_tramite.kardex.replace('T', ''))
                except ValueError:
                    last_number = 34
                next_number = last_number + 1
            else:
                next_number = 35

            self.kardex = f"T{next_number:03d}"

        super().save(*args, **kwargs)

class SeguimientoTramite(models.Model):
    ESTADO_CHOICES = [
        ('En proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
        ('Presentado', 'Presentado'),
    ]

    caso = models.ForeignKey(Tramite, on_delete=models.CASCADE, related_name='seguimientos_tramites')
    fecha_seguimiento = models.DateField(blank=True, null=True)
    seguimiento = HTMLField(null=True, blank=True)
    fecha_pendiente = models.DateField(blank=True, null=True)
    pendiente = HTMLField(null=True, blank=True)
    responsable = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_proceso')
    pdf = models.FileField(upload_to='seguimiento/', max_length=255, blank=True, null=True)
    inter = models.BooleanField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    editor = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='seguimientos_tramite_creados')
    fecha_alerta = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Seguimiento - {self.caso.tramite_tipo} - {self.fecha_seguimiento}"


class GastoTramite(models.Model):
    seguimiento = models.ForeignKey(SeguimientoTramite, on_delete=models.CASCADE, related_name='gastos_tramites')
    fecha = models.DateField()
    detalle = models.TextField(blank=True, null=True)
    sustento = models.TextField(blank=True)
    pdf = models.FileField(upload_to='gastos_expediente/', blank=True, null=True)
    codigo_pago = models.CharField(max_length=255, blank=True, null=True)
    gastos_soles = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gastos_dolares = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_registro2 = models.DateTimeField(auto_now=True)
    editor = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='seguimientos_gasto2')

    def __str__(self):
        return f"Gasto - {self.fecha}"
