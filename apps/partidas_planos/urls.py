from django.urls import path
from . import views

urlpatterns = [
    path('documentacion/', views.DocumentacionView.as_view(), name='documentacion'),
    
    path('partidas/', views.PartidaListView.as_view(), name='lista_partidas'),
    path('partidas/editar/', views.PartidaUpdateView.as_view(), name='editar_partida'),
    path('partidas/eliminar/<int:doc_id>/', views.PartidaDeleteView.as_view(), name='eliminar_partida'),

    path('planos/', views.PlanoListView.as_view(), name='lista_planos'),
    path('planos/editar/', views.PlanoUpdateView.as_view(), name='editar_plano'),
    path('planos/eliminar/<int:doc_id>/', views.PlanoDeleteView.as_view(), name='eliminar_plano'),
    path('sistemas/', views.SistemasView.as_view(), name='sistemas'),

]
