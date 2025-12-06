from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import ListView

from .models import Asistencia

"""
CODIGO ANTIGUO
@login_required
def home(request):
    user = request.user

    # Si es administrador → ve todo
    if user.role == user.ADMINISTRADOR or user.is_superuser:
        asistencias = Asistencia.objects.all().order_by('-fecha')

        # 🔹 Obtener lista única de trabajadores
        trabajadores = (
            Asistencia.objects
            .select_related('trabajador')
            .values('trabajador__id', 'trabajador__first_name', 'trabajador__last_name')
            .distinct()
            .order_by('trabajador__first_name')
        )

    else:
        # Si no es administrador → solo sus asistencias
        asistencias = Asistencia.objects.filter(trabajador=user).order_by('-fecha')
        trabajadores = []  # No necesita el filtro

    return render(
        request,
        'asistencia/detail.html',
        {'asistencias': asistencias, 'trabajadores': trabajadores}
    )
"""

""" migre el codigo a class based view es mucho mas escalable y limpio
"""
class AsistenciaView(LoginRequiredMixin, ListView):
    model = Asistencia
    template_name = 'asistencia/detail.html'
    context_object_name = 'asistencias'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.role == user.ADMINISTRADOR or user.is_superuser:
            return Asistencia.objects.all().order_by('-fecha')
        return Asistencia.objects.filter(trabajador=user).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.role == user.ADMINISTRADOR or user.is_superuser:
            context['trabajadores'] = (
                Asistencia.objects
                .select_related('trabajador')
                .values(
                    'trabajador__id',
                    'trabajador__first_name',
                    'trabajador__last_name'
                )
                .distinct()
                .order_by('trabajador__first_name')
            )
        else:
            context['trabajadores'] = []

        return context
