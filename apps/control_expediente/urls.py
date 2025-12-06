from django.urls import path
from . import views

app_name = 'control_expediente'

urlpatterns = [
    # CASO JUDICIAL
    path('', views.CasoJudicialListView.as_view(), name='lista_expediente'),
    path('<int:caso_id>/', views.CasoJudicialDetailView.as_view(), name='ver_seguimiento'),
    path('editar/', views.CasoJudicialUpdateView.as_view(), name='editar_expediente'),
    path('eliminar/<int:doc_id>/', views.CasoJudicialDeleteView.as_view(), name='eliminar_expediente'),
    
    # Nuevas rutas para crear
    path('crear-seguimiento/<int:caso_id>/', views.SeguimientoCreateView.as_view(), name='crear_seguimiento'),
    path('crear-gasto/', views.GastoCreateView.as_view(), name='crear_gasto'),

    path('editar-seguimiento/', views.SeguimientoUpdateView.as_view(), name='editar_seguimiento'),
    path('seguimiento-expediente/eliminar/<int:seguimiento_id>/', views.SeguimientoDeleteView.as_view(), name='eliminar_seguimiento'),

    path('editar-ce-gasto/', views.GastoUpdateView.as_view(), name='editar_gasto'),
    path('eliminar_ce_gasto/', views.GastoDeleteView.as_view(), name='eliminar_gasto'),

    path('actividad/', views.RegistroActividadListView.as_view(), name='lista_registros_actividad'),

    # EXPORTAR GASTOS A EXCEL
    path('exportar-gastos-excel/<int:caso_id>/', views.ExportarGastosExcelView.as_view(), name='exportar_gastos_excel'),
    path('exportar-gastos-fiscal-excel/<int:caso_id>/', views.ExportarGastosFiscalExcelView.as_view(), name='exportar_gastos_fiscal_excel'),

    # CARPETA FISCAL
    path('lista-carpeta-fiscal/', views.CarpetaFiscalListView.as_view(), name='lista_carpeta_fiscal'),
    path('editar-carpeta-fiscal/', views.CarpetaFiscalUpdateView.as_view(), name='editar_carpeta_fiscal'),
    path('eliminar-carpeta-fiscal/<int:doc_id>/', views.CarpetaFiscalDeleteView.as_view(), name='eliminar_carpeta_fiscal'),

    path('ver-seguimiento-carpeta-fiscal/<int:caso_id>/', views.CarpetaFiscalDetailView.as_view(), name='ver_seguimiento_carpeta_fiscal'),
    
    # Nuevas rutas para crear fiscal
    path('crear-seguimiento-fiscal/<int:caso_id>/', views.SeguimientoFiscalCreateView.as_view(), name='crear_seguimiento_fiscal'),
    path('crear-gasto-fiscal/', views.GastoFiscalCreateView.as_view(), name='crear_gasto_fiscal'),

    path('editar-seguimiento-carpeta-fiscal/', views.SeguimientoFiscalUpdateView.as_view(), name='editar_seguimiento_carpeta_fiscal'),
    path('seguimiento-carpeta-fiscal/eliminar/<int:seguimiento_id>/', views.SeguimientoFiscalDeleteView.as_view(), name='eliminar_seguimiento_carpeta_fiscal'),

    path('editar-ce-gasto-carpeta-fiscal/', views.GastoFiscalUpdateView.as_view(), name='editar_ce_gasto_carpeta_fiscal'),
    path('eliminar-gasto-carpeta-fiscal/', views.GastoFiscalDeleteView.as_view(), name='eliminar_gasto_carpeta_fiscal'),

    # CONCLUIDOS
    path('concluido/', views.CasoJudicialConcluidosListView.as_view(), name='lista_concluidos'),
    path('seguimiento-concluido/<int:caso_id>/', views.CasoJudicialConcluidoDetailView.as_view(), name='ver_seguimiento_concluido'),
    path('editar-exp-gen-concluido/', views.CasoJudicialToggleConcluidoView.as_view(), name='editar_expediente_general_concluido'),
    path('eliminar-exp-concluido/<int:doc_id>/', views.CasoJudicialConcluidoDeleteView.as_view(), name='eliminar_exp_concluido'),

    path('lista-concluidos-fiscal/', views.CarpetaFiscalConcluidosListView.as_view(), name='lista_concluidos_fiscal'),
    path('seguimiento-fiscal-concluido/<int:caso_id>/', views.CarpetaFiscalConcluidoDetailView.as_view(), name='ver_seguimiento_fiscal_concluido'),
    path('editar-exp-fiscal-concluido/', views.CarpetaFiscalToggleConcluidoView.as_view(), name='editar_expediente_fiscal_concluido'),
    path('eliminar-concluidos-fiscal/<int:doc_id>/', views.CarpetaFiscalConcluidoDeleteView.as_view(), name='eliminar_concluidos_fiscal'),
]