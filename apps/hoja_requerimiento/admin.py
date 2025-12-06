from django.contrib import admin
from .models import Q1_T1

@admin.register(Q1_T1)
class Q1_T1Admin(admin.ModelAdmin):
    list_display = ("fecha_vencimiento", "proveedor", "soles", "dolares")
    search_fields = ("proveedor", "concepto")