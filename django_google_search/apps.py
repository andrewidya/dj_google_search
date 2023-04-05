from django.apps import AppConfig


class DjangoGoogleSearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_google_search'

    def ready(self):
        from .signals import run_search
