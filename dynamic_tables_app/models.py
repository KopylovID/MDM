from django.db import models
from django.core.exceptions import ValidationError
from core.mixin import IDMixin, CreatedAtMixin, UpdatedAtMixin
import logging

logger = logging.getLogger(__name__)


class DynamicTableSchema(IDMixin, CreatedAtMixin, UpdatedAtMixin, models.Model):
    """Хранит описание всех созданных динамических таблиц"""

    schema_name = models.CharField(
        verbose_name="Схема объекта БД", # TODO: Локализация
        max_length=255,
        default="public",
    )

    object_name = models.CharField(
        verbose_name="Имя объекта  БД", # TODO: Локализация
        max_length=255,
        unique=True,
    )

    schema_json = models.JSONField(
        verbose_name="Схема таблицы",
        help_text="JSON с описанием полей",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Динамическая таблица"
        verbose_name_plural = "Динамические таблицы"
        ordering = ["-created_at"]
        db_table = '"meta_app"."dynamic_table_schema"'

    def __str__(self):
        return self.table_name

    @property
    def table_name(self):
        return f"{self.object_name}"

    @property
    def db_table_name(self):
        return f'"{self.schema_name}"."{self.object_name}"'

    def clean(self):
        """Валидация схемы"""
        if not isinstance(self.schema_json, dict):
            raise ValidationError("Описание таблицы должно быть словарем")

        if "fields" not in self.schema_json:
            raise ValidationError("Отсутствуют поля таблицы")

        if not isinstance(self.schema_json["fields"], list):
            raise ValidationError("Поля должны быт перечислены как список")

        for field in self.schema_json["fields"]:
            if "name" not in field or "type" not in field:
                raise ValidationError("Проверка отсутствия имени и типа поля")

    def get_manager(self):
        """Возвращает DynamicModelManager"""
        from .managers import DynamicModelManager

        schema = self.schema_json.copy()
        schema["table_name"] = self.table_name
        schema["app_label"] = "dynamic_tables_app"
        return DynamicModelManager(schema)

    def sync_table(self):
        """Создает/синхронизирует таблицу в БД"""
        manager = self.get_manager()
        manager.create_table()
        return manager

    @classmethod
    def create_from_schema(cls, schema: dict):
        """Создает запись о схеме и таблицу в БД"""

        # Создаем запись в БД
        schema_record = cls.objects.create(
            schema_name=schema["schema_name"], object_name=schema["table_name"], schema_json=schema
        )

        # Создаем физическую таблицу
        manager = schema_record.get_manager()
        manager.create_table()

        return schema_record

    @classmethod
    def restore_all(cls):
        """Восстанавливает все активные модели при старте приложения"""
        restored = []
        for schema_record in cls.objects.filter(is_active=True):
            try:
                manager = schema_record.get_manager()
                manager.get_model()  # Регистрирует модель
                restored.append(schema_record.table_name)
            except Exception as e:
                logger.error(f"Проблема с восстановлением: {schema_record.table_name}: {e}")
        return restored
