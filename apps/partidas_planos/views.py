import locale
import calendar

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models.functions import ExtractYear, ExtractMonth
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.urls import reverse_lazy

from .forms import PartidaForm, PlanoForm
from .models import Partida, Plano

User = get_user_model()

class SistemasView(LoginRequiredMixin, TemplateView):
    template_name = 'sistemas/index.html'

class DocumentacionView(LoginRequiredMixin, TemplateView):
    template_name = 'partidas_planos/home.html'

class PartidaListView(LoginRequiredMixin, CreateView):
    model = Partida
    form_class = PartidaForm
    template_name = 'partidas_planos/lista_partidas.html'
    success_url = reverse_lazy('lista_partidas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partidas'] = Partida.objects.all()

        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error:
            pass

        context['anios'] = (
            Partida.objects.annotate(anio=ExtractYear('fecha'))
            .values_list('anio', flat=True)
            .distinct()
            .order_by('anio')
        )

        meses_unicos = (
            Partida.objects.annotate(mes=ExtractMonth('fecha'))
            .values_list('mes', flat=True)
            .distinct()
            .order_by('mes')
        )
        context['meses'] = [(i, calendar.month_name[i]) for i in meses_unicos if i]
        return context

    def form_invalid(self, form):
        print("Errores del formulario:")
        print(form.errors)
        return super().form_invalid(form)

class PartidaUpdateView(LoginRequiredMixin, UpdateView):
    model = Partida
    form_class = PartidaForm
    success_url = reverse_lazy('lista_partidas')

    def get_object(self, queryset=None):
        return get_object_or_404(Partida, id=self.request.POST.get('id'))

    def form_invalid(self, form):
        print(form.errors)
        return redirect(self.success_url)

class PartidaDeleteView(LoginRequiredMixin, View):
    def get(self, request, doc_id):
        doc = get_object_or_404(Partida, id=doc_id)
        doc.delete()
        return redirect('lista_partidas')

class PlanoListView(LoginRequiredMixin, CreateView):
    model = Plano
    form_class = PlanoForm
    template_name = 'partidas_planos/lista_planos.html'
    success_url = reverse_lazy('lista_planos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planos'] = Plano.objects.all().order_by('fecha')

        context['anios'] = (
            Plano.objects.annotate(anio=ExtractYear('fecha'))
            .values_list('anio', flat=True)
            .distinct()
            .order_by('anio')
        )
        return context

class PlanoUpdateView(LoginRequiredMixin, UpdateView):
    model = Plano
    form_class = PlanoForm
    success_url = reverse_lazy('lista_planos')

    def get_object(self, queryset=None):
        return get_object_or_404(Plano, id=self.request.POST.get('id'))

    def form_invalid(self, form):
        print(form.errors)
        return redirect(self.success_url)

class PlanoDeleteView(LoginRequiredMixin, View):
    def get(self, request, doc_id):
        plano = get_object_or_404(Plano, id=doc_id)
        plano.delete()
        return redirect('lista_planos')
