from django.contrib import admin
from .models import *


class GastoInline(admin.TabularInline):
    model = Gasto
    extra = 1


class SeguimientoInline(admin.TabularInline):
    model = Seguimiento
    extra = 1


@admin.register(CasoJudicial)
class CasoJudicialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'expediente', 'sede', 'juzgado', 'representante')
    list_filter = ('representante', 'sede', 'especialidad', 'materia')
    search_fields = ('expediente', 'demandante', 'demandado', 'juzgado')
    inlines = [SeguimientoInline]

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('caso', 'fecha_seguimiento', 'responsable', 'estado')
    list_filter = ('estado', 'fecha_seguimiento')
    search_fields = ('caso__expediente', 'responsable', 'resolucion', 'seguimiento')
    inlines = [GastoInline]

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('seguimiento', 'fecha', 'detalle', 'gastos_soles', 'gastos_dolares')
    list_filter = ('fecha',)
    search_fields = ('detalle', 'sustento')

##################################################################################################################

@admin.register(CarpetaFiscal)
class CarpetaFiscalAdmin(admin.ModelAdmin):
    list_display = ('item', 'carpeta_fiscal', 'sede', 'fiscalia', 'representante')
    list_filter = ('representante', 'sede', 'especialidad', 'delito')
    search_fields = ('carpeta_fiscal', 'demandante', 'demandado', 'fiscalia')
    
@admin.register(SeguimientoFiscal)
class SeguimientoFiscalAdmin(admin.ModelAdmin):
    list_display = ('caso', 'fecha_seguimiento', 'responsable', 'estado')
    list_filter = ('estado', 'fecha_seguimiento')
    search_fields = ('caso__expediente', 'responsable', 'resolucion', 'seguimiento')

@admin.register(GastoFiscal)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('seguimiento', 'fecha', 'detalle', 'gastos_soles', 'gastos_dolares')
    list_filter = ('fecha',)
    search_fields = ('detalle', 'sustento')

