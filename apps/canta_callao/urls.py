from django.urls import path
from . import views

app_name = 'p_canta_callao'

urlpatterns = [
    path('lista_proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('editar_proyecto/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:doc_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),

    path('ver_actividades/<int:caso_id>/', views.ver_actividades, name='ver_actividades'),
    path('editar_actividad/', views.editar_actividad, name='editar_actividad'),
    # path('seguimiento_expediente/eliminar/<int:seguimiento_id>/', views.eliminar_seguimiento, name='eliminar_seguimiento'),

    # path('editar_ce_gasto/', views.editar_gasto, name='editar_gasto'),
    # path('eliminar_ce_gasto/', views.eliminar_gasto, name='eliminar_gasto'),


    # path('lista_registros_actividad/', views.lista_registros_actividad, name='lista_registros_actividad'),



    # # CARPETA FISCAL
    # path('lista_carpeta_fiscal/', views.lista_carpeta_fiscal, name='lista_carpeta_fiscal'),
    # path('editar_carpeta_fiscal/', views.editar_carpeta_fiscal, name='editar_carpeta_fiscal'),
    # path('eliminar_carpeta_fiscal/<int:doc_id>/', views.eliminar_carpeta_fiscal, name='eliminar_carpeta_fiscal'),

    # path('ver_seguimiento_carpeta_fiscal/<int:caso_id>/', views.ver_seguimiento_carpeta_fiscal, name='ver_seguimiento_carpeta_fiscal'),
    # path('editar_seguimiento_carpeta_fiscal/', views.editar_seguimiento_carpeta_fiscal, name='editar_seguimiento_carpeta_fiscal'),
    # path('seguimiento_carpeta_fiscal/eliminar/<int:seguimiento_id>/', views.eliminar_seguimiento_carpeta_fiscal, name='eliminar_seguimiento_carpeta_fiscal'),

    # path('editar_ce_gasto_carpeta_fiscal/', views.editar_ce_gasto_carpeta_fiscal, name='editar_ce_gasto_carpeta_fiscal'),
    # path('eliminar_gasto_carpeta_fiscal/', views.eliminar_gasto_carpeta_fiscal, name='eliminar_gasto_carpeta_fiscal'),
]