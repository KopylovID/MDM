from django.db import models
from .dic_object import DicObject
from core.models.base import BaseEntity
from .dic_attr_type import DicAttrType


class DicObjectColumn(BaseEntity):
    """Колонки объекта"""

    dictionary = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        on_delete=models.CASCADE,
        related_name="column",
        db_index=False,
    )

    column_name = models.CharField(
        verbose_name="Название колонки",  # TODO: Локализация
        max_length=255,
    )

    column_description = models.TextField(
        verbose_name="Детальное описание колонки",  # TODO: Локализация
        null=True,
    )

    column_type = models.ForeignKey(
        verbose_name="Тип колонки",  # TODO: Локализация
        to=DicAttrType,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    is_null = models.BooleanField(
        verbose_name="Обязательность",  # TODO: Локализация
        default=True,
    )

    ordinal_position = models.FloatField(
        verbose_name="Порядок следования",  # TODO: Локализация
        default=0.00,
    )

    is_pk = models.BooleanField(
        verbose_name="Первичный ключ",  # TODO: Локализация
        default=False,
    )

    class Meta:
        db_table = '"meta_app"."dic_object_column"'
