from django.contrib import admin
from .models import *

@admin.register(CentroDeCostos)
class CentroDeCostosAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(TipoDeGasto)
class TipoDeGastoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'centro_de_costos', 'tipo', 'responsable', 'fecha_registro')
    list_filter = ('tipo', 'centro_de_costos')
    search_fields = ('nombre', 'codigo', 'responsable')

@admin.register(GastoTA2020)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'fecha', 'documento', 'debe', 'haber', 'tipo_gasto', 'fecha_registro')
    list_filter = ('actividad', 'tipo_gasto', 'fecha')
    search_fields = ('nombre', 'detalle', 'documento')

@admin.register(NuevoGasto)
class NuevoGastoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'flag')
    list_filter = ('flag',)
    search_fields = ('nombre',)

#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
@admin.register(GastoN9)
class GastoN9Admin(admin.ModelAdmin):
    list_display = ('expediente', 'fecha', 'monto_soles', 'monto_dolares')
    search_fields = ('expediente', 'juzgado')
    list_filter = ('expediente', 'juzgado')

