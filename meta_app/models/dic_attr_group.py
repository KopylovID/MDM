from core.models.base import BaseEntity, BaseDTO
from django.db import models
from dataclasses import dataclass
import json


class DicAttrGroup(BaseEntity):
    """Группа атрибутов"""

    group_code = models.CharField(
        verbose_name="Код группы",  # TODO: Локализация
        max_length=255,
        unique=True,
    )
    group_name = models.CharField(
        verbose_name="Наименование группы",  # TODO: Локализация
        max_length=255,
    )
    group_description = models.TextField(
        verbose_name="Детальное описание группы",  # TODO: Локализация
        null=True,
    )

    group_params = models.JSONField(
        verbose_name="Параметры группы",  # TODO: Локализация
        null=True,
    )

    class Meta:
        db_table = '"meta_app"."dic_attr_group"'


@dataclass
class DicAttrGroupDTO(BaseDTO):
    group_code: str
    group_name: str
    group_description: str
    group_params: json = None
