from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Anios, Q1_T1
from .forms import AniosForm, Q1_T1Form

class HojaRequerimientoHomeView(ListView):
    model = Anios
    template_name = 'hoja_requerimiento/home.html'
    context_object_name = 'ngs'

    def get_queryset(self):
        return Anios.objects.filter(flag=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AniosForm()
        return context

class ListaQ1T1View(LoginRequiredMixin, CreateView):
    model = Q1_T1
    form_class = Q1_T1Form
    template_name = 'hoja_requerimiento/lista_q1_t1.html'
    success_url = reverse_lazy('hoja_requerimiento:lista_q1_t1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gasto_general'] = Q1_T1.objects.all()
        context['nombreN1'] = Anios.objects.first()
        return context