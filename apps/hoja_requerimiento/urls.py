from django.urls import path
from . import views

app_name = 'hoja_requerimiento'

urlpatterns = [
    path('hoja-requerimiento-home/', views.HojaRequerimientoHomeView.as_view(), name='hoja_requerimiento_home'),
    path('lista-q1-t1/', views.ListaQ1T1View.as_view(), name='lista_q1_t1'),
]
