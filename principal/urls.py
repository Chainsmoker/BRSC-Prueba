from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('accounts/asistencia/', include('apps.asistencia.urls')),
    path('accounts/my/', views.perfil_user, name='perfil_user'),

    path('costos/', include('apps.centro_costos.urls')),
    path('expedientes/', include('apps.control_expediente.urls')),

    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario'),
    path('editar_CC/', views.editar_CC, name='editar_CC'),
    path('eliminar_CC/<int:id>/', views.eliminar_CC, name='eliminar_CC'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('cambiar_password_usuario/', views.cambiar_password_usuario, name='cambiar_password_usuario'),

    path('', include('apps.partidas_planos.urls')),
    path('', include('apps.hoja_requerimiento.urls')),
    path('', include('apps.tramites.urls')),
    path('', include('apps.canta_callao.urls')),
    path('productivity/', include('apps.productividad.urls')),
    path('ia/', views.int_art, name='int_art'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ⚠️ Esto permite servir archivos aunque DEBUG=False (solo para pruebas)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)