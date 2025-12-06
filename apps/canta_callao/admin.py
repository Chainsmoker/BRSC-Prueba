# from django.contrib import admin
# from .models import Proyecto, Actividad


# class ActividadInline(admin.TabularInline):
#     model = Actividad
#     extra = 1
#     fields = ('descripcion', 'fecha', 'debe', 'haber', 'saldo', 'sustento')
#     readonly_fields = ('fecha_creacion', 'fecha_modificacion')
#     show_change_link = True


# @admin.register(Proyecto)
# class ProyectoAdmin(admin.ModelAdmin):
#     list_display = ('proyecto', 'presupuesto', 'fecha', 'fecha_creacion', 'fecha_modificacion')
#     list_filter = ('fecha', 'fecha_creacion')
#     search_fields = ('proyecto',)
#     readonly_fields = ('fecha_creacion', 'fecha_modificacion')
#     inlines = [ActividadInline]
#     date_hierarchy = 'fecha'
#     ordering = ('-fecha_creacion',)


# @admin.register(Actividad)
# class ActividadAdmin(admin.ModelAdmin):
#     list_display = ('descripcion', 'proyecto', 'fecha', 'debe', 'haber', 'saldo')
#     list_filter = ('fecha', 'proyecto')
#     search_fields = ('descripcion', 'proyecto__proyecto')
#     readonly_fields = ('fecha_creacion', 'fecha_modificacion')
#     date_hierarchy = 'fecha'
#     ordering = ('-fecha',)
