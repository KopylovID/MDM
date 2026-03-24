from .base import BaseEntity
from django.db import models
from .dic_attr_type import DicAttrType
from .dic_attr_group import DicAttrGroup

class DicObjectAttr(BaseEntity):
    """Атрибуты объектов"""

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
        null=True,
    )

    attr_type = models.ForeignKey(
        verbose_name="Тип атрибута",  # TODO: Локализация
        to=DicAttrType,
        on_delete=models.CASCADE,
        related_name='+', # Отключаем обратное обращение
        related_query_name='+', # Отключаем фильтрацию
    )

    attr_group = models.ForeignKey(
        verbose_name="Группа атрибута",  # TODO: Локализация
        to=DicAttrGroup,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+', # Отключаем обратное обращение
        related_query_name='+', # Отключаем фильтрацию
    )

    class Meta:
        db_table = "meta\".\"dic_object_attr"