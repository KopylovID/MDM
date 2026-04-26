from typing import Dict, Any, List, Optional
from .models import DynamicTableSchema


class DynamicTableService:
    """Сервис для работы с динамическими таблицами"""

    @staticmethod
    def create_table(schema: Dict[str, Any]) -> DynamicTableSchema:
        """
        Создает новую динамическую таблицу

        Пример schema:
        {
            'table_name': 'Product',
            'fields': [
                {'name': 'name', 'type': 'CharField', 'max_length': 200},
                {'name': 'price', 'type': 'DecimalField', 'max_digits': 10, 'decimal_places': 2},
            ]
        }
        """
        return DynamicTableSchema.create_from_schema(schema)

    @staticmethod
    def get_table(table_name: str) -> Optional[DynamicTableSchema]:
        """Получает информацию о таблице"""
        try:
            return DynamicTableSchema.objects.get(object_name=table_name, is_active=True)
        except DynamicTableSchema.DoesNotExist:
            return None

    @staticmethod
    def delete_table(table_name: str, drop_db_table: bool = True) -> bool:
        """Удаляет динамическую таблицу"""
        try:
            schema_record = DynamicTableSchema.objects.get(object_name=table_name)

            if drop_db_table:
                manager = schema_record.get_manager()
                manager.drop_table()

            schema_record.is_active = False
            schema_record.save()
            return True
        except DynamicTableSchema.DoesNotExist:
            return False

    @staticmethod
    def list_tables() -> List[Dict]:
        """Список всех динамических таблиц"""
        return list(DynamicTableSchema.objects.filter(is_active=True).values("object_name"))

    @staticmethod
    def get_data(table_name: str, filters: Dict = None, page: int = 1, page_size: int = 100):
        """Получает данные из динамической таблицы"""
        schema_record = DynamicTableService.get_table(table_name)
        if not schema_record:
            raise ValueError(f"Таблица '{table_name}' не найдена")

        manager = schema_record.get_manager()
        queryset = manager.all()

        if filters:
            queryset = queryset.filter(**filters)

        total = queryset.count()
        offset = (page - 1) * page_size
        items = list(queryset.values()[offset : offset + page_size])

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }

    @staticmethod
    def create_record(table_name: str, data: Dict) -> Dict:
        """Создает запись в динамической таблице"""
        schema_record = DynamicTableService.get_table(table_name)
        if not schema_record:
            raise ValueError(f"Таблица '{table_name}' не найдена")

        manager = schema_record.get_manager()
        instance = manager.create(**data)

        # Возвращаем словарь с данными созданной записи
        return {field.name: getattr(instance, field.name) for field in instance._meta.fields}

    @staticmethod
    def update_record(table_name: str, record_id: int, data: Dict) -> int:
        """Обновляет запись в динамической таблице"""
        schema_record = DynamicTableService.get_table(table_name)
        if not schema_record:
            raise ValueError(f"Таблица '{table_name}' не найдена")

        manager = schema_record.get_manager()
        return manager.update(record_id, **data)

    @staticmethod
    def delete_record(table_name: str, record_id: int) -> int:
        """Удаляет запись из динамической таблицы"""
        schema_record = DynamicTableService.get_table(table_name)
        if not schema_record:
            raise ValueError(f"Таблица '{table_name}' не найдена")

        manager = schema_record.get_manager()
        return manager.delete(record_id)
