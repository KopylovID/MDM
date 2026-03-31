from django.db import models

from .base import BaseEntity
from .dic_object import DicObject
from .dic_attr import DicAttr
from .dic_attr_type import DicAttrType
from .mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
)

# TODO: Рефакторинг+. Необходимо разделить хранение каждого типа значения на отдельную таблицу


class DicObjectAttrValue(
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    models.Model,
):
    """Класс значений атрибутов справочника"""

    dictionary = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    attribute = models.ForeignKey(
        verbose_name="Идентификатор атрибута справочника",  # TODO: Локализация
        to=DicAttr,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    attr_type = models.ForeignKey(
        verbose_name="Тип атрибута",  # TODO: Локализация
        to=DicAttrType,
        on_delete=models.CASCADE,
        related_name='+',  # Отключаем обратное обращение
        related_query_name='+',  # Отключаем фильтрацию
        db_index=False,
    )

    value = models.TextField(
        verbose_name="Значение атрибута",  # TODO: Локализация
    )

    value_params = models.JSONField(
        verbose_name="Параметры значения атрибута",  # TODO: Локализация
        null=True,
    )

    class Meta:
        db_table = '"meta"."dic_object_attr_value"'
