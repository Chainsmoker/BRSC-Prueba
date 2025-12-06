from django.urls import path
from . import views

app_name = 'tramites'

urlpatterns = [
    path('tramites/', views.ListaTramiteView.as_view(), name='lista_tramite'),
    path('tramites/editar/', views.EditarTramiteView.as_view(), name='editar_tramite'),
    path('tramites/eliminar/<int:doc_id>/', views.EliminarTramiteView.as_view(), name='eliminar_tramite'),

    path('tramites/<int:caso_id>/', views.VerSeguimientoTramiteView.as_view(), name='ver_seguimiento_tramite'),
    path('editar_seguimiento_tramite/', views.EditarSeguimientoTramiteView.as_view(), name='editar_seguimiento_tramite'),
    path('eliminar_seguimiento_tramite/eliminar/<int:seguimiento_tramite_id>/', views.EliminarSeguimientoTramiteView.as_view(), name='eliminar_seguimiento_tramite'),

    path('editar_gasto_tramite/', views.EditarGastoTramiteView.as_view(), name='editar_gasto_tramite'),
    path('eliminar_gasto_tramite/', views.EliminarGastoTramiteView.as_view(), name='eliminar_gasto_tramite'),

    path('exportar_gastos_tramite_excel/<int:caso_id>/', views.ExportarGastosTramiteExcelView.as_view(), name='exportar_gastos_tramite_excel'),

    # CONCLUIDOS
    path('tramites/concluidos/', views.ListaTramiteConcluidosView.as_view(), name='lista_tramite_concluidos'),
    path('ver_seguimiento_t_concluido/<int:caso_id>/', views.VerSeguimientoTramiteConcluidoView.as_view(), name='ver_seguimiento_t_concluido'),
    path('editar_t_concluido/', views.EditarTramiteConcluidoView.as_view(), name='editar_t_concluido'),
]