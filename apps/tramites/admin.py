from django.contrib import admin
from .models import Tramite, SeguimientoTramite, GastoTramite

@admin.register(Tramite)
class TramiteAdmin(admin.ModelAdmin):
    list_display = ('kardex', 'tramite_tipo', 'fecha', 'destinatario')
    search_fields = ('kardex', 'tramite_tipo', 'destinatario')
    readonly_fields = ('kardex',)
    list_filter = ('tramite_tipo',)

@admin.register(SeguimientoTramite)
class SeguimientoTramiteAdmin(admin.ModelAdmin):
    list_display = ('caso', 'fecha_seguimiento', 'estado')
    search_fields = ('caso__tramite_tipo', 'estado')
    list_filter = ('estado',)

@admin.register(GastoTramite)
class GastoTramiteAdmin(admin.ModelAdmin):
    list_display = ('seguimiento', 'fecha', 'gastos_soles', 'gastos_dolares', 'codigo_pago')
    search_fields = ('seguimiento__caso__tramite_tipo', 'detalle', 'codigo_pago')
    list_filter = ('fecha',)