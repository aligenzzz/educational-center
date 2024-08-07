from django.apps import AppConfig


class ApiAuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_authentication'
    
    def ready(self):
        import api_authentication.signals
