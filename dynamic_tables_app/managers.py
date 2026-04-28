from django.db import models, connection
from django.apps import apps
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class DynamicModelManager:
    """Менеджер для создания динамических моделей и работы с ними"""

    def __init__(self, schema: Dict[str, Any]):
        """
        schema: словарь с описанием таблицы
        {
            'table_name': 'Product',
            'app_label': 'dynamic_tables_app',
            'fields': [...]
        }
        """
        self.schema = schema
        self.table_name = schema["table_name"]
        self.db_table = f'"{schema["schema_name"]}"."{schema["table_name"]}"'
        self.app_label = schema.get("app_label", "dynamic_tables_app")
        self.model: Optional[type] = None

    def _get_django_field(self, field_def: Dict) -> models.Field:
        """Преобразует описание поля в Django Field"""
        field_def = field_def.copy()


        field_type = field_def.get("type")

        # Общие параметры
        common_params = ['verbose_name', 'help_text', 'db_index', 'unique', 'default']

        # Специфичные параметры для разных типов
        specific_params = {
            'CharField': ['max_length', 'min_length', 'choices'],
            'TextField': ['max_length'],
            'IntegerField': ['min_value', 'max_value'],
            'DecimalField': ['max_digits', 'decimal_places', 'min_value', 'max_value'],
            'BooleanField': [],
            'DateTimeField': ['auto_now', 'auto_now_add'],
            'DateField': ['auto_now', 'auto_now_add'],
            'FloatField': ['min_value', 'max_value'],
            'JSONField': ['encoder', 'decoder'],
            'AutoField': ['primary_key']
        }

        # Все допустимые параметры
        allowed_params = common_params + specific_params.get(field_type, [])

        field_mapping = {
            "CharField": models.CharField,
            "TextField": models.TextField,
            "IntegerField": models.IntegerField,
            "BigIntegerField": models.BigIntegerField,
            "DecimalField": models.DecimalField,
            "BooleanField": models.BooleanField,
            "DateTimeField": models.DateTimeField,
            "DateField": models.DateField,
            "FloatField": models.FloatField,
            "JSONField": models.JSONField,
            "AutoField": models.AutoField
        }

        field_class = field_mapping.get(field_type)
        if not field_class:
            raise ValueError(f"Не поддерживаемый тип данных: {field_type}")

        if field_type == "DecimalField":
            if "max_digits" not in field_def:
                field_def["max_digits"] = 10
            if "decimal_places" not in field_def:
                field_def["decimal_places"] = 2

        if field_type in ("CharField", "TextField"):
            if "max_length" not in field_def and field_type != "TextField":
                field_def["max_length"] = 255

        if field_type == "AutoField":
            field_def["primary_key"] = True

        # Фильтруем параметры
        filtered_params = {}
        for key, value in field_def.items():

            if key == 'is_null':
                filtered_params['null'] = not value

            if key == 'is_pk':
                filtered_params['unique'] = False if value is None else value

            # Пропускаем служебные параметры
            if key in ['type']:
                continue

            # Оставляем только допустимые параметры
            elif key in allowed_params:
                filtered_params[key] = value

        return field_class(**filtered_params)

    def create_model(self) -> type:
        """Создает класс модели из описания"""

        class Meta:
            app_label = self.app_label
            db_table = self.db_table
            managed = False  # Отключение автоматических миграций

        attrs = {
            "__module__": f"{self.app_label}.dynamic_models",
            "Meta": Meta,
        }

        # Добавляем поля
        for field_def in self.schema["fields"]:
            field_name = field_def.get("name")
            attrs[field_name] = self._get_django_field(field_def)

        # Добавляем ID если его нет
        if "id" not in attrs:
            attrs["id"] = models.AutoField(primary_key=True)

        # Добавляем метод __str__
        def __str__(self):
            first_field = "id"
            return str(getattr(self, first_field, self.id))

        attrs["__str__"] = __str__

        # Создаем класс модели
        model_class = type(self.table_name, (models.Model,), attrs)

        # Регистрируем модель
        try:
            apps.register_model(self.app_label, model_class)
        except RuntimeError:
            pass # Модель зарегистрирована

        self.model = model_class
        logger.info(f"Модель '{self.table_name}' успешно создана")
        return model_class

    def get_model(self) -> type:
        """Получаем существующую модель или создаем новую"""
        if self.model:
            return self.model

        try:
            model = apps.get_model(self.app_label, self.table_name)
            self.model = model
            return model
        except LookupError:
            return self.create_model()

    def table_exists(self) -> bool:
        """Проверка существования таблицы в БД"""
        from django.db import connection

        return self.table_name in connection.introspection.table_names()

    def create_table(self) -> bool:
        if self.table_exists():
            logger.info(f"Таблица '{self.table_name}' уже существует")
            return False

        model = self.get_model()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)
        logger.info(f"Таблица '{self.table_name}' создана")
        return True

    def drop_table(self) -> bool:
        """Удаляем таблицу из БД"""
        if not self.table_exists():
            return False

        model = self.get_model()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(model)
        logger.info(f"Таблица '{self.table_name}' удалена")
        return True

    def create(self, **kwargs) -> models.Model:
        """Создание записи"""
        model = self.get_model()
        return model.objects.create(**kwargs)

    def get(self, id: int) -> models.Model:
        """Получение записи по id"""
        model = self.get_model()
        return model.objects.get(pk=id)

    def filter(self, **kwargs) -> models.QuerySet:
        """Фильтрация записей"""
        model = self.get_model()
        return model.objects.filter(**kwargs)

    def all(self) -> models.QuerySet:
        """Все записи"""
        model = self.get_model()
        return model.objects.all()

    def update(self, id: int, **kwargs) -> int:
        """Обновление записи"""
        model = self.get_model()
        return model.objects.filter(pk=id).update(**kwargs)

    def delete(self, id: int) -> int:
        """Удаление записи"""
        model = self.get_model()
        _, deleted = model.objects.filter(pk=id).delete()
        return deleted

    def count(self) -> int:
        """Количество записей"""
        model = self.get_model()
        return model.objects.count()