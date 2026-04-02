from .base import BaseEntity
from django.db import models
from .dic_attr import DicAttr
from .dic_object_attr_value import DicObjectAttrValue
from .mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
)


class DicObjectAttrValueRelation(
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    models.Model,
):
    """Связанные параметры значений атрибутов"""

    object_attr_value = models.ForeignKey(
        verbose_name="ИД на значение атрибута объекта",  # TODO: Локализация
        to=DicObjectAttrValue,
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
    value = models.TextField(
        verbose_name="Значение атрибута",  # TODO: Локализация
        null=True,
    )

    value_params = models.JSONField(
        verbose_name="Параметры значения атрибута",  # TODO: Локализация
        null=True,
    )

    class Meta:
        db_table = '"meta"."dic_object_attr_value_ralation"'
