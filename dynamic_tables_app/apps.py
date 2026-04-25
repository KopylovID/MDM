from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class DynamicTablesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dynamic_tables_app"
    verbose_name = 'Динамические таблицы'

    def ready(self):
        """При запуске приложения восстанавливаем все динамические модели"""
        from .models import DynamicTableSchema

        # Пытаемся восстановить модели, если таблица схем уже существует
        try:
            restored = DynamicTableSchema.restore_all()
            if restored:
                logger.info(f"Восстановленные модели: {', '.join(restored)}")
        except Exception as e:
            logger.debug(f"Ошибка при восстановлении моделей: {e}")