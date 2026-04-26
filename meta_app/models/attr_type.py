from core.models.base import BaseEntity, BaseDTO
from django.db import models
from dataclasses import dataclass
import json


class AttrType(BaseEntity):
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

    tech_type_name = models.CharField(
        verbose_name="Техническое название",  # TODO: Локализация
        max_length=255,
        null=True,
    )

    type_params = models.JSONField(
        verbose_name="Параметры типа",  # TODO: Локализация
        null=True,
    )

    class Meta:
        db_table = '"meta_app"."attr_type"'

    def __str__(self):
        return f"{self.type_name}"


@dataclass
class AttrTypeDTO(BaseDTO):
    type_code: str
    type_name: str
    type_description: str
    tech_type_name: str
    type_params: json = None
