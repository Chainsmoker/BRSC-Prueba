from django.apps import AppConfig

class ControlExpedienteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.control_expediente'

    def ready(self):
        import apps.control_expediente.signals
