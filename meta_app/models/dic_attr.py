from .base import BaseEntity, BaseDTO
from django.db import models
from .dic_attr_type import DicAttrType
from .dic_attr_group import DicAttrGroup
from dataclasses import dataclass, asdict
import json
from typing import Dict


class DicAttr(BaseEntity):
    """Атрибуты объектов"""

    attr_code = models.CharField(
        verbose_name="Код атрибута", # TODO: Локализация
        max_length=255,
        unique=True,
    )

    attr_name = models.CharField(
        verbose_name="Наименование атрибута",  # TODO: Локализация
        max_length=255,
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


@dataclass
class DicAttrDTO(BaseDTO):
    attr_code: str
    attr_name: str
    attr_description: str
    __attr_type__: str
    __attr_group__: str
    attr_params: json = None

    attr_type: DicAttrType = None
    attr_group: DicAttrGroup = None
