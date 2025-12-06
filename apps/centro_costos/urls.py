from django.urls import path
from . import views

app_name = 'centro_costos'

urlpatterns = [
    path('', views.CentroCostosHomeView.as_view(), name='home'),

    path('actividades/', views.ActividadListView.as_view(), name='lista_actividades'),
    path('editar-actividad/', views.ActividadUpdateView.as_view(), name='editar_actividad'),
    path('eliminar-actividad/<int:doc_id>/', views.ActividadDeleteView.as_view(), name='eliminar_actividad'),
    
    path('gastos/tupac-amaru/', views.GastoTA2020ListView.as_view(), name='lista_gastos'),
    path('editar-gasto/', views.GastoTA2020UpdateView.as_view(), name='editar_gasto'),
    path('eliminar-gasto/<int:doc_id>/', views.GastoTA2020DeleteView.as_view(), name='eliminar_gasto'),

    path('gastos/canta-callao/', views.CantaCallaoListView.as_view(), name='lista_canta_callao'),
    path('gastos/canta-callao/editar/', views.CantaCallaoUpdateView.as_view(), name='editar_canta_callao'),
    path('gastos/canta-callao/eliminar/<int:doc_id>/', views.CantaCallaoDeleteView.as_view(), name='eliminar_canta_callao'),

    path('agregar-nuevo-gasto/', views.AgregarNuevoGastoView.as_view(), name='agregar_nuevo_gasto'),

    path('gastos/proyecto/<int:pk>/', views.GastoGenericListView.as_view(), name='lista_gastos_proyecto'),
    path('gastos/editar/', views.GastoGenericUpdateView.as_view(), name='editar_gasto_generico'),
    path('gastos/eliminar/<int:doc_id>/', views.GastoGenericDeleteView.as_view(), name='eliminar_gasto_generico'),

    path('lista-gastoN9/', views.GastoN9ListView.as_view(), name='lista_gastoN9'),
    path('editar-gastoN9/', views.GastoN9UpdateView.as_view(), name='editar_gastoN9'),
    path('eliminar-gastoN9/<int:doc_id>/', views.GastoN9DeleteView.as_view(), name='eliminar_gastoN9'),

    path('tupac-amaru/', views.HomeTAView.as_view(), name='home_ta'),
    path('canta-callao/', views.HomeCCView.as_view(), name='home_cc'),
]
