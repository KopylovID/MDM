from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class DynamicTablesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dynamic_tables_app"
    verbose_name = 'Динамические таблицы'

    def ready(self):
        """При запуске приложения восстанавливаем все динамические модели"""

        from django.core.signals import request_started
        from .models import DynamicTableSchema

        request_started.connect(lambda sender, **kwargs: DynamicTableSchema.restore_all())