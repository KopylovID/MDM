from .base import BaseEntity, BaseDTO
from django.db import models
from dataclasses import dataclass
import json


class DicAttrType(BaseEntity):
    """Тип атрибута"""

    type_code = models.CharField(
        verbose_name="Код типа",  # TODO: Локализация
        max_length=255,
        unique=True,
    )
    type_name = models.CharField(
        verbose_name="Наименование типа",  # TODO: Локализация
        max_length=255,
    )
    type_description = models.TextField(
        verbose_name="Детальное описание типа",  # TODO: Локализация
        null=True,
    )

    type_params = models.JSONField(
        verbose_name="Параметры типа",  # TODO: Локализация
        null=True,
    )

    class Meta:
        db_table = '"meta"."dic_attr_type"'

@dataclass
class DicAttrTypeDTO(BaseDTO):
    type_code: str
    type_name: str
    type_description: str
    type_params: json = None