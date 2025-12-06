from django.utils import timezone
from .models import RegistroActividad

class RegistroActividadMixin:
    """
    Mixin para registrar actividad automáticamente al crear, actualizar o eliminar objetos.
    """
    actividad_accion = None  
    actividad_modelo = None 

    def form_valid(self, form):
        response = super().form_valid(form)
        self.registrar_actividad(self.object)
        return response

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        self.registrar_actividad(self.object, accion="Eliminó")
        return response

    def registrar_actividad(self, objeto, accion=None):
        if not self.request.user.is_authenticated:
            return

        accion = accion or self.actividad_accion or "Modificó"
        modelo = self.actividad_modelo or objeto._meta.verbose_name
        
        descripcion = str(objeto)
        
        if hasattr(objeto, 'expediente'):
            descripcion = objeto.expediente
        elif hasattr(objeto, 'carpeta_fiscal'):
            descripcion = objeto.carpeta_fiscal

        mensaje = f"{accion} {modelo}: {descripcion}"
        
        RegistroActividad.objects.create(
            nombre=f"{self.request.user.first_name} {self.request.user.last_name}".strip(),
            fecha=timezone.now(),
            actividad=mensaje,
            user=self.request.user
        )
