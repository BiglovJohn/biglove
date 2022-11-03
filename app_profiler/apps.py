from django.apps import AppConfig


class ProfilerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_profiler'
    verbose_name = 'Профили пользователей'
