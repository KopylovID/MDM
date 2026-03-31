from .base import BaseEntity
from django.db import models
from dataclasses import dataclass


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

    class Meta:
        db_table = '"meta"."dic_attr_group"'


@dataclass
class DicAttrGroupDTO:
    group_code: str
    group_name: str
    group_description: str
