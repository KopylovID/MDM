from core.models.base import BaseEntity, BaseDTO
from django.db import models
from .attr_type import AttrType
from .attr_group import AttrGroup
from dataclasses import dataclass
import json


class Attr(BaseEntity):
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
        to=AttrType,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
        db_index=False,
    )

    attr_group = models.ForeignKey(
        verbose_name="Группа атрибута",  # TODO: Локализация
        to=AttrGroup,
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
        db_table = '"meta_app"."attr"'


@dataclass
class AttrDTO(BaseDTO):
    attr_code: str
    attr_name: str
    attr_description: str
    __attr_type__: str
    __attr_group__: str
    attr_params: json = None

    attr_type: AttrType = None
    attr_group: AttrGroup = None
