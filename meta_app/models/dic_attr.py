from .base import BaseEntity
from django.db import models
from .dic_attr_type import DicAttrType
from .dic_attr_group import DicAttrGroup


class DicAttr(BaseEntity):
    """Атрибуты объектов"""

    attr_name = models.CharField(verbose_name="Наименование атрибута", max_length=255)  # TODO: Локализация

    attr_code = models.CharField(
        verbose_name="Код атрибута", max_length=255, unique=True, null=True  # TODO: Локализация
    )

    attr_description = models.TextField(
        verbose_name="Детальное описание атрибута",  # TODO: Локализация
        null=True,
    )

    attr_type = models.ForeignKey(
        verbose_name="Тип атрибута",  # TODO: Локализация
        to=DicAttrType,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    attr_group = models.ForeignKey(
        verbose_name="Группа атрибута",  # TODO: Локализация
        to=DicAttrGroup,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    attr_params = models.JSONField(
        verbose_name="Параметры атрибута",  # TODO: Локализация
        null=True,
    )

    class Meta:
        db_table = '"meta"."dic_attr"'
