from base import BaseEntity
from django.db import models
from .dic_attr_type import DicAttrType

class DicObjectAttr(BaseEntity):
    """Класс атрибуттов справочника"""

    attr_name = models.CharField(
        verbose_name="Наименование атрибута",  # TODO: Локализация
        max_length=255
    )

    attr_code = models.CharField(
        verbose_name="Код атрибута",  # TODO: Локализация
        max_length=255,
        unique=True,
        null=True
    )

    attr_description = models.TextField(
        verbose_name="Детальное описание атрибута",  # TODO: Локализация
    )

    attr_type_id = models.ForeignKey(
        verbose_name="Тип атрибута",  # TODO: Локализация
        to=DicAttrType,
        related_name='+', # Отключаем обратное обращение
        related_query_name='+', # Отключаем фильтрацию
    )

    class Meta:
        db_table = "dic_object_attr"