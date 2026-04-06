from django.db import models
from .attr import Attr
from .object_attr_value import ObjectAttrValue
from core.mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
)


class ObjectAttrValueRelation(
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
        to=ObjectAttrValue,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    attribute = models.ForeignKey(
        verbose_name="Идентификатор атрибута справочника",  # TODO: Локализация
        to=Attr,
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
        db_table = '"meta_app"."object_attr_value_ralation"'
