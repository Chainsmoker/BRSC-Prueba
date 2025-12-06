from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db.models.functions import Substr, ExtractYear, ExtractMonth
from django.db.models import Sum, Q
from django.utils import timezone

from apps.control_expediente.models import RegistroActividad

from .forms import *
from .models import *

User = get_user_model()

class HomeTAView(LoginRequiredMixin, TemplateView):
    template_name = 'centro_costos/home_ta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['proyecto_2024'] = NuevoGasto.objects.all()[1]
        except IndexError:
            context['proyecto_2024'] = None
        return context

class HomeCCView(LoginRequiredMixin, TemplateView):
    template_name = 'centro_costos/home_cc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['proyecto_2024'] = NuevoGasto.objects.all()[1]
        except IndexError:
            context['proyecto_2024'] = None
        return context

class CentroCostosHomeView(View):
    def get(self, request):
        ngs = NuevoGasto.objects.filter(flag=True)
        form = NuevoGastoForm()
        return render(request, 'centro_costos/home.html', {
            'ngs': ngs,
            'form': form,
        })

class AgregarNuevoGastoView(View):
    def post(self, request):
        form = NuevoGastoForm(request.POST)
        if form.is_valid():
            try:
                nuevo_gasto = NuevoGasto.objects.filter(flag=False).first()
                if nuevo_gasto:
                    nuevo_gasto.nombre = form.cleaned_data['nombre']
                    nuevo_gasto.flag = True
                    nuevo_gasto.save()
                    RegistroActividad.objects.create(
                        nombre=f"{request.user.first_name} {request.user.last_name}".strip(),
                        fecha=timezone.now(),
                        actividad=f"[CENTRO COSTOS] Agregó nuevo centro de costos: {nuevo_gasto.nombre}",
                        user_id=request.user.id,
                    )
            except NuevoGasto.DoesNotExist:
                pass
        return redirect('centro_costos:home')

class ActividadListView(LoginRequiredMixin, CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'centro_costos/lista_actividades.html'
    success_url = reverse_lazy('centro_costos:lista_actividades')

    def post(self, request, *args, **kwargs):
        nuevo_centro = request.POST.get('nuevo_centro_de_costos', '').strip()
        if nuevo_centro:
            centro_obj, created = CentroDeCostos.objects.get_or_create(nombre=nuevo_centro)
            request.POST = request.POST.copy()
            request.POST['centro_de_costos'] = centro_obj.id
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actividades'] = Actividad.objects.all()
        context['centros_de_costos'] = CentroDeCostos.objects.all()
        return context

class ActividadUpdateView(LoginRequiredMixin, UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'centro_costos/lista_actividades.html'
    success_url = reverse_lazy('centro_costos:lista_actividades')

    def get_object(self, queryset=None):
        actividad_id = self.request.POST.get('id')
        return get_object_or_404(Actividad, id=actividad_id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actividades'] = Actividad.objects.all()
        context['centros_de_costos'] = CentroDeCostos.objects.all()
        return context

class ActividadDeleteView(LoginRequiredMixin, DeleteView):
    model = Actividad
    success_url = reverse_lazy('centro_costos:lista_actividades')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Actividad, id=self.kwargs['doc_id'])

class GastoTA2020ListView(LoginRequiredMixin, CreateView):
    model = GastoTA2020
    form_class = GastoTA2020Form
    template_name = 'centro_costos/lista_gastos.html'
    success_url = reverse_lazy('centro_costos:lista_gastos')

    def post(self, request, *args, **kwargs):
        nuevo_tipo = request.POST.get('nuevo_tipo_gasto', '').strip()
        if nuevo_tipo:
            tipo_obj, created = TipoDeGasto.objects.get_or_create(nombre=nuevo_tipo)
            request.POST = request.POST.copy()
            request.POST['tipo_gasto'] = tipo_obj.id
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gastos'] = GastoTA2020.objects.all().order_by('fecha')
        context['tipos_de_gasto'] = TipoDeGasto.objects.all()
        context['actividades'] = Actividad.objects.all()
        return context

class GastoTA2020UpdateView(LoginRequiredMixin, UpdateView):
    model = GastoTA2020
    form_class = GastoTA2020Form
    template_name = 'centro_costos/lista_gastos.html'
    success_url = reverse_lazy('centro_costos:lista_gastos')

    def get_object(self, queryset=None):
        gasto_id = self.request.POST.get('id')
        return get_object_or_404(GastoTA2020, id=gasto_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gastos'] = GastoTA2020.objects.all().order_by('fecha')
        context['tipos_de_gasto'] = TipoDeGasto.objects.all()
        context['actividades'] = Actividad.objects.all()
        return context

class GastoTA2020DeleteView(LoginRequiredMixin, DeleteView):
    model = GastoTA2020
    success_url = reverse_lazy('centro_costos:lista_gastos')
    
    def get_object(self, queryset=None):
        return get_object_or_404(GastoTA2020, id=self.kwargs['doc_id'])
    
    def post(self, request, *args, **kwargs):
        from django.http import JsonResponse
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

class CantaCallaoListView(LoginRequiredMixin, CreateView):
    model = CantaCallao
    form_class = CantaCallaoForm
    template_name = 'centro_costos/lista_canta_callao.html'
    success_url = reverse_lazy('centro_costos:lista_canta_callao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canta_callao'] = CantaCallao.objects.annotate(
            anio=Substr('codigo', 8, 2),
            idinterno=Substr('codigo', 4, 3),
        ).order_by('anio', 'idinterno')
        return context

class CantaCallaoUpdateView(LoginRequiredMixin, UpdateView):
    model = CantaCallao
    form_class = CantaCallaoForm
    template_name = 'centro_costos/lista_canta_callao.html'
    success_url = reverse_lazy('centro_costos:lista_canta_callao')

    def get_object(self, queryset=None):
        canta_callao_id = self.request.POST.get('id')
        return get_object_or_404(CantaCallao, id=canta_callao_id)

class CantaCallaoDeleteView(LoginRequiredMixin, DeleteView):
    model = CantaCallao
    template_name = 'centro_costos/lista_canta_callao.html'
    success_url = reverse_lazy('centro_costos:lista_canta_callao')
    
    def get_object(self, queryset=None):
        return get_object_or_404(CantaCallao, id=self.kwargs['doc_id'])
    
    def post(self, request, *args, **kwargs):
        from django.http import JsonResponse
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

class GastoGenericListView(LoginRequiredMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    
    def get_origen(self):
        return get_object_or_404(NuevoGasto, pk=self.kwargs['pk'])

    def get_queryset(self):
        origen = self.get_origen()
        return Gasto.objects.filter(origen=origen)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        origen = self.get_origen()
        gastos = self.get_queryset()

        total_soles_egresos = gastos.filter(es_ingreso=False).aggregate(total=Sum('monto_soles'))['total'] or 0
        total_soles_ingresos = gastos.filter(es_ingreso=True).aggregate(total=Sum('monto_soles'))['total'] or 0
        context['total_soles'] = total_soles_egresos - total_soles_ingresos

        total_dolares_egresos = gastos.filter(es_ingreso=False).aggregate(total=Sum('monto_dolares'))['total'] or 0
        total_dolares_ingresos = gastos.filter(es_ingreso=True).aggregate(total=Sum('monto_dolares'))['total'] or 0
        context['total_dolares'] = total_dolares_egresos - total_dolares_ingresos

        context['anios'] = (
            Gasto.objects.filter(origen=origen).annotate(anio=ExtractYear('fecha'))
            .values_list('anio', flat=True)
            .distinct()
            .order_by('anio')
        )
        
        context['gasto_general'] = gastos
        context['proyecto'] = origen
        context['editores'] = Gasto.objects.filter(origen=origen).values_list('editor', flat=True).distinct()
        return context

    def form_valid(self, form):
        gasto = form.save(commit=False)
        gasto.editor = f"{self.request.user.first_name} {self.request.user.last_name}"
        origen = self.get_origen()
        gasto.origen = origen
        gasto.save()

        RegistroActividad.objects.create(
            nombre=f"{self.request.user.first_name} {self.request.user.last_name}".strip(),
            fecha=timezone.now(),
            actividad=f"[{origen.nombre}] Agregó un nuevo gasto",
            user_id=self.request.user.id,
        )
        return redirect('centro_costos:lista_gastos_proyecto', pk=origen.pk)
    
    def get_template_names(self):
        return ['centro_costos/lista_proyecto.html']

class GastoGenericUpdateView(LoginRequiredMixin, UpdateView):
    model = Gasto
    form_class = GastoForm
    
    def get_object(self, queryset=None):
        gasto_id = self.request.POST.get('id')
        return get_object_or_404(Gasto, id=gasto_id)

    def get_success_url(self):
        return reverse_lazy('centro_costos:lista_gastos_proyecto', kwargs={'pk': self.object.origen.pk})

class GastoGenericDeleteView(LoginRequiredMixin, DeleteView):
    model = Gasto
    
    def get_object(self, queryset=None):
        return get_object_or_404(Gasto, id=self.kwargs['doc_id'])

    def get_success_url(self):
        return reverse_lazy('centro_costos:lista_gastos_proyecto', kwargs={'pk': self.object.origen.pk})
    
    def post(self, request, *args, **kwargs):
        from django.http import JsonResponse
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

class GastoN9ListView(LoginRequiredMixin, CreateView):
    model = GastoN9
    form_class = GastoN9Form
    template_name = 'centro_costos/lista_gastoN9.html'
    success_url = reverse_lazy('centro_costos:lista_gastoN9')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gasto_general'] = GastoN9.objects.all()
        nuevo_gastos = NuevoGasto.objects.all()
        context['nombreN9'] = nuevo_gastos[8] if nuevo_gastos.count() > 8 else None
        
        context['anios'] = (
            GastoN9.objects
            .exclude(fecha__isnull=True)
            .annotate(anio=ExtractYear('fecha'))
            .values_list('anio', flat=True)
            .distinct()
            .order_by('anio')
        )

        context['expedientes_unicos'] = (
            GastoN9.objects
            .exclude(expediente__isnull=True)
            .exclude(expediente__exact="")
            .values_list('expediente', flat=True)
            .distinct()
            .order_by('expediente')
        )
        return context

class GastoN9UpdateView(LoginRequiredMixin, UpdateView):
    model = GastoN9
    form_class = GastoN9Form
    template_name = 'centro_costos/lista_gastoN9.html'
    success_url = reverse_lazy('centro_costos:lista_gastoN9')

    def get_object(self, queryset=None):
        gasto_id = self.request.POST.get('id')
        return get_object_or_404(GastoN9, id=gasto_id)

class GastoN9DeleteView(LoginRequiredMixin, DeleteView):
    model = GastoN9
    success_url = reverse_lazy('centro_costos:lista_gastoN9')
    
    def get_object(self, queryset=None):
        return get_object_or_404(GastoN9, id=self.kwargs['doc_id'])

