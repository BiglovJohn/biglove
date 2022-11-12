from django.apps import AppConfig


class AppAutoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_auto'
