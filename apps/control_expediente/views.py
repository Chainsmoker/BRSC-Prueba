import openpyxl

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.db.models import OuterRef, Subquery, DateField, TextField, ExpressionWrapper, F, DateTimeField
from django.utils import timezone
from django.db import connection
from django.http import HttpResponse
from datetime import date

from .models import (
    CasoJudicial, Seguimiento, Gasto, 
    CarpetaFiscal, SeguimientoFiscal, GastoFiscal, 
    RegistroActividad, User
)
from .forms import (
    CasoJudicialForm, SeguimientoForm, GastoForm,
    CarpetaFiscalForm, SeguimientoFiscalForm, GastoFiscalForm
)
from .mixins import RegistroActividadMixin
from .utils import to_decimal

class ExportarGastosExcelView(LoginRequiredMixin, View):
    is_fiscal = False

    def get(self, request, caso_id):
        return self.exportar_gastos_excel_logic(caso_id, self.is_fiscal)

    def exportar_gastos_excel_logic(self, caso_id, is_fiscal=False):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Gastos"

        headers = ["Expediente", "Resolución", "Fecha", "Detalle", "Código Pago", "Gasto (S/)", "Gasto ($)"]
        if is_fiscal:
            headers[0] = "Expediente Penal"
        ws.append(headers)

        table_gasto = "control_expediente_gastofiscal" if is_fiscal else "control_expediente_gasto"
        table_seguimiento = "control_expediente_seguimientofiscal" if is_fiscal else "control_expediente_seguimiento"
        table_caso = "control_expediente_carpetafiscal" if is_fiscal else "control_expediente_casojudicial"
        col_caso = "carpeta_fiscal" if is_fiscal else "expediente"

        query = f"""
            SELECT 
                c.{col_caso},
                s.resolucion,
                g.fecha,
                g.detalle,
                g.codigo_pago,
                g.gastos_soles,
                g.gastos_dolares
            FROM {table_gasto} AS g
            INNER JOIN {table_seguimiento} AS s ON g.seguimiento_id = s.id
            INNER JOIN {table_caso} AS c ON s.caso_id = c.id
            WHERE c.id = %s
            ORDER BY s.resolucion ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [caso_id])
            for row in cursor.fetchall():
                ws.append(row)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        filename = f"gastos_expediente_{caso_id}.xlsx"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

class ExportarGastosFiscalExcelView(ExportarGastosExcelView):
    is_fiscal = True

class RegistroActividadListView(LoginRequiredMixin, ListView):
    model = RegistroActividad
    template_name = 'control_expediente/registro_actividad.html'
    context_object_name = 'registro_actividad'
    ordering = ['-fecha']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_legales'] = (
            User.objects.filter(is_active=True)
            .exclude(username__in=['plupa', 'cdiaz'])
            .order_by('first_name')
        )
        return context

class CasoJudicialListView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = CasoJudicial
    form_class = CasoJudicialForm
    template_name = 'control_expediente/home.html'
    success_url = reverse_lazy('control_expediente:lista_expediente')
    actividad_accion = 'Registró'
    actividad_modelo = 'un nuevo expediente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        hoy = date.today()
        subquery_seguimiento_alerta = (
            Seguimiento.objects
            .filter(caso=OuterRef('pk'), fecha_alerta__gte=hoy)
            .order_by('fecha_alerta', '-fecha_registro')
        )
        subquery_fecha_alerta = subquery_seguimiento_alerta.values('fecha_alerta')[:1]
        subquery_pendiente_alerta = subquery_seguimiento_alerta.values('pendiente')[:1]

        caso_judiciales = (
            CasoJudicial.objects
            .annotate(
                proxima_alerta=Subquery(subquery_fecha_alerta, output_field=DateField()),
                pendiente_alerta=Subquery(subquery_pendiente_alerta, output_field=TextField())
            )
            .exclude(concluido=False)
            .select_related('responsable')
            .order_by('codigo')
        )

        for cj in caso_judiciales:
            if cj.proxima_alerta:
                dias_restantes = (cj.proxima_alerta - hoy).days
                if dias_restantes <= 5:
                    cj.alerta_color = "danger"
                elif dias_restantes <= 15:
                    cj.alerta_color = "warning"
                else:
                    cj.alerta_color = "success"
            else:
                cj.alerta_color = "secondary"

        context['caso_judiciales'] = caso_judiciales
        
        context['especialidades'] = (
            CasoJudicial.objects
            .exclude(especialidad__isnull=True)
            .exclude(especialidad__exact="")
            .values_list('especialidad', flat=True)
            .distinct()
            .order_by('especialidad')
        )
        context['usuarios_legales'] = User.objects.filter(role=User.LEGAL, is_active=True).order_by('first_name')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.concluido = True
        self.object.save()
        self.registrar_actividad(self.object)
        return redirect(self.success_url)

class CasoJudicialConcluidosListView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = CasoJudicial
    form_class = CasoJudicialForm
    template_name = 'control_expediente/concluidos.html'
    success_url = reverse_lazy('control_expediente:lista_concluidos')
    actividad_accion = 'Registró'
    actividad_modelo = 'un nuevo expediente (concluido)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caso_judiciales'] = (
            CasoJudicial.objects
            .exclude(concluido=True)
            .prefetch_related('seguimientos')
        )
        context['especialidades'] = (
            CasoJudicial.objects.exclude(especialidad__isnull=True)
            .exclude(especialidad__exact="")
            .values_list('especialidad', flat=True)
            .distinct()
            .order_by('especialidad')
        )
        context['usuarios_legales'] = User.objects.filter(role=User.LEGAL, is_active=True).order_by('first_name')
        return context

class CasoJudicialUpdateView(LoginRequiredMixin, RegistroActividadMixin, UpdateView):
    model = CasoJudicial
    form_class = CasoJudicialForm
    success_url = reverse_lazy('control_expediente:lista_expediente')
    actividad_accion = 'Modificó'
    actividad_modelo = 'el expediente'

    def get_object(self, queryset=None):
        return get_object_or_404(CasoJudicial, id=self.request.POST.get('id'))

class CasoJudicialDeleteView(LoginRequiredMixin, RegistroActividadMixin, DeleteView):
    model = CasoJudicial
    success_url = reverse_lazy('control_expediente:lista_expediente')
    actividad_accion = 'Eliminó'
    actividad_modelo = 'el expediente'

    def get_object(self, queryset=None):
        return get_object_or_404(CasoJudicial, id=self.kwargs['doc_id'])

class CasoJudicialConcluidoDeleteView(LoginRequiredMixin, RegistroActividadMixin, DeleteView):
    model = CasoJudicial
    success_url = reverse_lazy('control_expediente:lista_concluidos')
    actividad_accion = 'Eliminó'
    actividad_modelo = 'el expediente concluido'

    def get_object(self, queryset=None):
        return get_object_or_404(CasoJudicial, id=self.kwargs['doc_id'])

class CasoJudicialToggleConcluidoView(LoginRequiredMixin, RegistroActividadMixin, View):
    def post(self, request, *args, **kwargs):
        cj_id = request.POST.get('id')
        cj = get_object_or_404(CasoJudicial, id=cj_id)
        cj.concluido = not cj.concluido
        cj.save()
        
        estado = "concluido" if not cj.concluido else "activo"
        RegistroActividad.objects.create(
            nombre=f"{request.user.first_name} {request.user.last_name}".strip(),
            fecha=timezone.now(),
            actividad=f"Cambió estado a {estado} el expediente: {cj.expediente}",
            user=request.user
        )
        return redirect('control_expediente:lista_concluidos')

class SeguimientoCreateView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = Seguimiento
    form_class = SeguimientoForm
    actividad_accion = 'Agregó'
    actividad_modelo = 'nuevo seguimiento en el expediente'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        caso_id = self.kwargs.get('caso_id')
        self.object.caso = get_object_or_404(CasoJudicial, id=int(caso_id))
        self.object.usuario = self.request.user
        self.object.editor = f"{self.request.user.first_name} {self.request.user.last_name}"
        self.object.save()
        
        self.registrar_actividad(self.object, accion="Agregó nuevo seguimiento en el expediente")
        return redirect('control_expediente:ver_seguimiento', caso_id=self.object.caso.id)

class GastoCreateView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    actividad_accion = 'Registró'
    actividad_modelo = 'un nuevo gasto'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        seguimiento_id = self.request.POST.get('seguimiento_id')
        self.object.seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
        self.object.editor = f"{self.request.user.first_name} {self.request.user.last_name}".strip() or self.request.user.username
        self.object.save()
        
        self.registrar_actividad(self.object, accion="Registró un nuevo gasto")
        return redirect('control_expediente:ver_seguimiento', caso_id=self.object.seguimiento.caso.id)

class CasoJudicialDetailView(LoginRequiredMixin, DetailView):
    model = CasoJudicial
    template_name = 'control_expediente/seguimientos_y_gastos.html'
    context_object_name = 'caso'
    pk_url_kwarg = 'caso_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = self.object
        
        context['form'] = SeguimientoForm()
        context['form2'] = GastoForm()

        seguimientos = (
            caso.seguimientos.all()
            .prefetch_related('gastos')
            .order_by('-fecha_seguimiento', '-fecha_registro')
        )
        
        total_soles = 0
        total_dolares = 0
        for s in seguimientos:
            for g in s.gastos.all():
                total_soles += g.gastos_soles or 0
                total_dolares += g.gastos_dolares or 0
            s.nombre_usuario = f"{s.usuario.first_name} {s.usuario.last_name}" if s.usuario else "—"

        context['seguimientos'] = seguimientos
        context['total_soles'] = total_soles
        context['total_dolares'] = total_dolares
        context['nombre_usuario'] = f"{self.request.user.first_name} {self.request.user.last_name}"
        
        context['especialidades'] = (
            CasoJudicial.objects.exclude(especialidad__isnull=True)
            .exclude(especialidad__exact="")
            .values_list('especialidad', flat=True)
            .distinct()
            .order_by('especialidad')
        )

        primer_gasto = Gasto.objects.filter(seguimiento__caso=caso).order_by('fecha').first()
        primera_fecha_gasto = primer_gasto.fecha if primer_gasto else None
        context['primera_fecha_gasto'] = primera_fecha_gasto

        query = """
            SELECT 
                c.expediente, s.resolucion, g.fecha, g.detalle, g.codigo_pago, g.gastos_soles, g.gastos_dolares
            FROM control_expediente_gasto AS g
            INNER JOIN control_expediente_seguimiento AS s ON g.seguimiento_id = s.id
            INNER JOIN control_expediente_casojudicial AS c ON s.caso_id = c.id
            WHERE c.id = %s
        """
        params = [caso.id]
        if primera_fecha_gasto:
            query += " AND g.fecha >= %s"
            params.append(primera_fecha_gasto)
        query += " ORDER BY s.resolucion ASC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        context['gastos_expediente'] = [
            {
                "expediente": row[0], "resolucion": row[1], "fecha": row[2],
                "detalle": row[3], "codigo_pago": row[4],
                "gastos_soles": row[5], "gastos_dolares": row[6],
            } for row in rows
        ]
        return context

class CasoJudicialConcluidoDetailView(CasoJudicialDetailView):
    template_name = 'control_expediente/seguimientos_y_gastos_concluidos.html'

class SeguimientoUpdateView(LoginRequiredMixin, RegistroActividadMixin, UpdateView):
    model = Seguimiento
    form_class = SeguimientoForm
    actividad_accion = 'Modificó'
    actividad_modelo = 'seguimiento del expediente'

    def get_object(self, queryset=None):
        return get_object_or_404(Seguimiento, id=self.request.POST.get('id'))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.editor = f"{self.request.user.first_name} {self.request.user.last_name}".strip()
        self.object.save()
        self.registrar_actividad(self.object)
        return redirect('control_expediente:ver_seguimiento', caso_id=self.object.caso.id)

class SeguimientoDeleteView(LoginRequiredMixin, RegistroActividadMixin, DeleteView):
    model = Seguimiento
    actividad_accion = 'Eliminó'
    actividad_modelo = 'seguimiento del expediente'

    def get_object(self, queryset=None):
        return get_object_or_404(Seguimiento, id=self.kwargs['seguimiento_id'])

    def get_success_url(self):
        return reverse_lazy('control_expediente:ver_seguimiento', kwargs={'caso_id': self.object.caso.id})

class GastoUpdateView(LoginRequiredMixin, RegistroActividadMixin, UpdateView):
    model = Gasto
    form_class = GastoForm
    actividad_accion = 'Modificó'
    actividad_modelo = 'gasto del expediente'

    def get_object(self, queryset=None):
        return get_object_or_404(Gasto, id=self.request.POST.get('id'))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.registrar_actividad(self.object)
        return redirect('control_expediente:ver_seguimiento', caso_id=self.object.seguimiento.caso.id)

class GastoDeleteView(LoginRequiredMixin, RegistroActividadMixin, View):
    def post(self, request, *args, **kwargs):
        gasto_id = request.POST.get('gasto_id')
        gasto = get_object_or_404(Gasto, id=gasto_id)
        caso_id = gasto.seguimiento.caso.id
        
        saldo_actual = request.user.saldo or Decimal("0")
        monto = (gasto.gastos_soles or Decimal("0")) + ((gasto.gastos_dolares or Decimal("0")) * Decimal("3.5"))
        request.user.saldo = saldo_actual + monto
        request.user.save()

        gasto.delete()
        
        RegistroActividad.objects.create(
            nombre=f"{request.user.first_name} {request.user.last_name}".strip(),
            fecha=timezone.now(),
            actividad=f"Eliminó un gasto del expediente: {gasto.seguimiento.caso.expediente}",
            user=request.user
        )
        return redirect('control_expediente:ver_seguimiento', caso_id=caso_id)

class CarpetaFiscalListView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = CarpetaFiscal
    form_class = CarpetaFiscalForm
    template_name = 'control_expediente/home_carpeta_fiscal.html'
    success_url = reverse_lazy('control_expediente:lista_carpeta_fiscal')
    actividad_accion = 'Registró'
    actividad_modelo = 'un nuevo expediente fiscal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caso_judiciales'] = CarpetaFiscal.objects.all().exclude(concluido=False)
        context['registro_actividad'] = RegistroActividad.objects.all()
        context['especialidades'] = (
            CarpetaFiscal.objects.exclude(especialidad__isnull=True)
            .exclude(especialidad__exact="")
            .values_list('especialidad', flat=True)
            .distinct()
            .order_by('especialidad')
        )
        context['usuarios_legales'] = User.objects.filter(role=User.LEGAL, is_active=True).order_by('first_name')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.concluido = True
        self.object.save()
        self.registrar_actividad(self.object)
        return redirect(self.success_url)

class CarpetaFiscalConcluidosListView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = CarpetaFiscal
    form_class = CarpetaFiscalForm
    template_name = 'control_expediente/home_carpeta_fiscal_concluidos.html'
    success_url = reverse_lazy('control_expediente:lista_carpeta_fiscal')
    actividad_accion = 'Registró'
    actividad_modelo = 'un nuevo expediente fiscal (concluido)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caso_judiciales'] = CarpetaFiscal.objects.all().exclude(concluido=True)
        context['registro_actividad'] = RegistroActividad.objects.all()
        context['especialidades'] = (
            CarpetaFiscal.objects.exclude(especialidad__isnull=True)
            .exclude(especialidad__exact="")
            .values_list('especialidad', flat=True)
            .distinct()
            .order_by('especialidad')
        )
        context['usuarios_legales'] = User.objects.filter(role=User.LEGAL, is_active=True).order_by('first_name')
        return context

class CarpetaFiscalUpdateView(LoginRequiredMixin, RegistroActividadMixin, UpdateView):
    model = CarpetaFiscal
    form_class = CarpetaFiscalForm
    success_url = reverse_lazy('control_expediente:lista_carpeta_fiscal')
    actividad_accion = 'Modificó'
    actividad_modelo = 'el expediente fiscal'

    def get_object(self, queryset=None):
        return get_object_or_404(CarpetaFiscal, id=self.request.POST.get('id'))

class CarpetaFiscalDeleteView(LoginRequiredMixin, RegistroActividadMixin, DeleteView):
    model = CarpetaFiscal
    success_url = reverse_lazy('control_expediente:lista_carpeta_fiscal')
    actividad_accion = 'Eliminó'
    actividad_modelo = 'el expediente fiscal'

    def get_object(self, queryset=None):
        return get_object_or_404(CarpetaFiscal, id=self.kwargs['doc_id'])

class CarpetaFiscalConcluidoDeleteView(LoginRequiredMixin, RegistroActividadMixin, DeleteView):
    model = CarpetaFiscal
    success_url = reverse_lazy('control_expediente:lista_concluidos_fiscal')
    actividad_accion = 'Eliminó'
    actividad_modelo = 'el expediente fiscal concluido'

    def get_object(self, queryset=None):
        return get_object_or_404(CarpetaFiscal, id=self.kwargs['doc_id'])

class CarpetaFiscalToggleConcluidoView(LoginRequiredMixin, RegistroActividadMixin, View):
    def post(self, request, *args, **kwargs):
        cj_id = request.POST.get('id')
        cj = get_object_or_404(CarpetaFiscal, id=cj_id)
        cj.concluido = not cj.concluido
        cj.save()
        
        estado = "concluido" if not cj.concluido else "no concluido"
        
        RegistroActividad.objects.create(
            nombre=f"{request.user.first_name} {request.user.last_name}".strip(),
            fecha=timezone.now(),
            actividad=f"Marcó como {estado} el expediente: {cj.carpeta_fiscal}",
            user=request.user
        )
        return redirect('control_expediente:lista_concluidos_fiscal')

class SeguimientoFiscalCreateView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = SeguimientoFiscal
    form_class = SeguimientoFiscalForm
    actividad_accion = 'Agregó'
    actividad_modelo = 'nuevo seguimiento fiscal'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        caso_id = self.kwargs.get('caso_id')
        self.object.caso = get_object_or_404(CarpetaFiscal, id=caso_id)
        self.object.usuario = self.request.user
        self.object.editor = f"{self.request.user.first_name} {self.request.user.last_name}"
        self.object.save()
        
        self.registrar_actividad(self.object, accion="Agregó nuevo seguimiento fiscal")
        return redirect('control_expediente:ver_seguimiento_carpeta_fiscal', caso_id=self.object.caso.id)

class GastoFiscalCreateView(LoginRequiredMixin, RegistroActividadMixin, CreateView):
    model = GastoFiscal
    form_class = GastoFiscalForm
    actividad_accion = 'Registró'
    actividad_modelo = 'un nuevo gasto fiscal'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        seguimiento_id = self.request.POST.get('seguimiento_id')
        self.object.seguimiento = get_object_or_404(SeguimientoFiscal, id=seguimiento_id)
        self.object.editor = f"{self.request.user.first_name} {self.request.user.last_name}".strip() or self.request.user.username
        self.object.save()
        
        self.registrar_actividad(self.object, accion="Registró un nuevo gasto fiscal")
        return redirect('control_expediente:ver_seguimiento_carpeta_fiscal', caso_id=self.object.seguimiento.caso.id)

class CarpetaFiscalDetailView(LoginRequiredMixin, DetailView):
    model = CarpetaFiscal
    template_name = 'control_expediente/seguimientos_y_gastos_fiscal.html'
    context_object_name = 'caso'
    pk_url_kwarg = 'caso_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = self.object
        
        context['form'] = SeguimientoFiscalForm()
        context['form2'] = GastoFiscalForm()

        seguimientos = (
            caso.seguimientos_penal.all()
            .prefetch_related('gastos_fiscal')
            .order_by('-fecha_seguimiento')
        )
        
        total_soles = 0
        total_dolares = 0
        for s in seguimientos:
            for g in s.gastos_fiscal.all():
                total_soles += g.gastos_soles or 0
                total_dolares += g.gastos_dolares or 0
            s.nombre_usuario = f"{s.usuario.first_name} {s.usuario.last_name}" if s.usuario else "—"

        context['seguimientos'] = seguimientos
        context['total_soles'] = total_soles
        context['total_dolares'] = total_dolares
        context['nombre_usuario'] = f"{self.request.user.first_name} {self.request.user.last_name}"
        
        context['especialidades'] = (
            CarpetaFiscal.objects.exclude(especialidad__isnull=True)
            .exclude(especialidad__exact="")
            .values_list('especialidad', flat=True)
            .distinct()
            .order_by('especialidad')
        )

        primer_gasto = GastoFiscal.objects.filter(seguimiento__caso=caso).order_by('fecha').first()
        primera_fecha_gasto = primer_gasto.fecha if primer_gasto else None
        context['primera_fecha_gasto'] = primera_fecha_gasto

        # Raw SQL
        query = """
            SELECT 
                c.carpeta_fiscal, s.resolucion, g.fecha, g.detalle, g.codigo_pago, g.gastos_soles, g.gastos_dolares
            FROM control_expediente_gastofiscal AS g
            INNER JOIN control_expediente_seguimientofiscal AS s ON g.seguimiento_id = s.id
            INNER JOIN control_expediente_carpetafiscal AS c ON s.caso_id = c.id
            WHERE c.id = %s
        """
        params = [caso.id]
        if primera_fecha_gasto:
            query += " AND g.fecha >= %s"
            params.append(primera_fecha_gasto)
        query += " ORDER BY g.fecha ASC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        context['gastos_expediente'] = [
            {
                "expediente": row[0], "resolucion": row[1], "fecha": row[2],
                "detalle": row[3], "codigo_pago": row[4],
                "gastos_soles": row[5], "gastos_dolares": row[6],
            } for row in rows
        ]
        return context

class CarpetaFiscalConcluidoDetailView(CarpetaFiscalDetailView):
    template_name = 'control_expediente/seguimientos_y_gastos_fiscal_concluidos.html'

class SeguimientoFiscalUpdateView(LoginRequiredMixin, RegistroActividadMixin, UpdateView):
    model = SeguimientoFiscal
    form_class = SeguimientoFiscalForm
    actividad_accion = 'Modificó'
    actividad_modelo = 'seguimiento fiscal'

    def get_object(self, queryset=None):
        return get_object_or_404(SeguimientoFiscal, id=self.request.POST.get('id'))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.editor = f"{self.request.user.first_name} {self.request.user.last_name}".strip()
        
        if self.request.POST.get('eliminar_pdf') == 'true' and self.object.pdf:
            self.object.pdf.delete(save=False)
            self.object.pdf = None
        
        nuevo_pdf = self.request.FILES.get('pdf')
        if nuevo_pdf:
            if self.object.pdf:
                self.object.pdf.delete(save=False)
            self.object.pdf = nuevo_pdf

        self.object.save()
        self.registrar_actividad(self.object)
        return redirect('control_expediente:ver_seguimiento_carpeta_fiscal', caso_id=self.object.caso.id)

class SeguimientoFiscalDeleteView(LoginRequiredMixin, RegistroActividadMixin, DeleteView):
    model = SeguimientoFiscal
    actividad_accion = 'Eliminó'
    actividad_modelo = 'seguimiento fiscal'

    def get_object(self, queryset=None):
        return get_object_or_404(SeguimientoFiscal, id=self.kwargs['seguimiento_id'])

    def get_success_url(self):
        return reverse_lazy('control_expediente:ver_seguimiento_carpeta_fiscal', kwargs={'caso_id': self.object.caso.id})

class GastoFiscalUpdateView(LoginRequiredMixin, RegistroActividadMixin, UpdateView):
    model = GastoFiscal
    form_class = GastoFiscalForm
    actividad_accion = 'Modificó'
    actividad_modelo = 'gasto fiscal'

    def get_object(self, queryset=None):
        return get_object_or_404(GastoFiscal, id=self.request.POST.get('id'))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'pdf' in self.request.FILES:
            self.object.pdf = self.request.FILES['pdf']
        self.object.save()
        self.registrar_actividad(self.object)
        return redirect('control_expediente:ver_seguimiento_carpeta_fiscal', caso_id=self.object.seguimiento.caso.id)

class GastoFiscalDeleteView(LoginRequiredMixin, RegistroActividadMixin, View):
    def post(self, request, *args, **kwargs):
        gasto_id = request.POST.get('gasto_id')
        gasto = get_object_or_404(GastoFiscal, id=gasto_id)
        caso_id = gasto.seguimiento.caso.id
        gasto.delete()
        
        RegistroActividad.objects.create(
            nombre=f"{request.user.first_name} {request.user.last_name}".strip(),
            fecha=timezone.now(),
            actividad=f"Eliminó un gasto del expediente: {gasto.seguimiento.caso.carpeta_fiscal}",
            user=request.user
        )
        return redirect('control_expediente:ver_seguimiento_carpeta_fiscal', caso_id=caso_id)
