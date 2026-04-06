from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from dataclasses import dataclass
from core.models import BaseEntity, BaseDTO
import json


class Structure(MPTTModel, BaseEntity):
    """Структура дерева папок справочников"""

    structure_parent = TreeForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    structure_code = models.CharField(
        verbose_name="Код структуры",  # TODO: Локализация
        max_length=255,
        unique=True,
    )
    structure_name = models.CharField(
        verbose_name="Наименование структуры",  # TODO: Локализация
        max_length=255,
    )
    structure_description = models.TextField(
        verbose_name="Детальное описание структуры",  # TODO: Локализация
    )

    class Meta:
        db_table = '"meta_app"."structure"'

    class MPTTMeta:
        parent_attr = 'structure_parent'  # поле родитель


@dataclass
class StructureDTO(BaseDTO):
    structure_code: str
    structure_name: str
    structure_description: str
    __params__: json = None

    structure_parent: Structure = None