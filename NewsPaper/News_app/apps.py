from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News_app'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
        