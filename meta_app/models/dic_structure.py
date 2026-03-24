from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin
)


class DicStructure(
    MPTTModel,
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin
):
    """Структура дерева папок справочников"""

    structure_parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
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
        db_table = "meta\".\"dic_structure"