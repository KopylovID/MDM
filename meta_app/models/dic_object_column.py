from django.db import models
from .dic_object import DicObject
from .dic_object_attr import DicObjectAttr
from .dic_attr_type import DicAttrType
from .dic_object_attr_value import DicObjectAttrValueStr
from .mixin import (
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin
)


class DicObjectColumn(
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    models.Model,
):
    """Колонки объекта"""

    id = models.OneToOneField(
        verbose_name="Идентификатор колонки",  # TODO: Локализация
        to=DicObjectAttrValueStr,
        on_delete=models.CASCADE,
        related_name="attribute",
        primary_key=True
    )

    uuid = models.UUIDField(
        verbose_name="Уникальный идентификатор записи",  # TODO: Локализация
        unique=True,
        editable=False,  # нельзя редактировать в админке
    )

    dictionary_id = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        on_delete=models.CASCADE,
        related_name="column",
    )

    column_name = models.CharField(
        verbose_name="Название колонки",  # TODO: Локализация
        max_length=255,
    )

    column_description = models.TextField(
        verbose_name="Детальное описание колонки",  # TODO: Локализация
        null=True,
    )

    column_type_id = models.ForeignKey(
        verbose_name="Тип колонки",  # TODO: Локализация
        to=DicAttrType,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
    )

    is_null = models.BooleanField(
        verbose_name="Обязательность",  # TODO: Локализация
        default=True,
    )

    ordinal_position = models.FloatField(
        verbose_name="Порядок следования", # TODO: Локализация
        default=0.0,
    )

    is_pk = models.BooleanField(
        verbose_name="Первичный ключ",  # TODO: Локализация
        default=False,
    )

    def save(self, id, uuid, *args, **kwargs):
        self.id = id
        self.uuid = uuid
        super().save(*args, **kwargs)

    class Meta:
        db_table = "dic_object_column"