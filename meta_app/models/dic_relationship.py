from django.db import models
from .base import BaseEntity
from .dic_object_column import DicObjectColumn


class DicRelationship(BaseEntity):
    """Отношения"""

    foreign_column = models.ForeignKey(
        verbose_name="ИД колонки",  # TODO: Локализация
        to=DicObjectColumn,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
    )

    references_column = models.ForeignKey(
        verbose_name="ИД ссылочной колонки",  # TODO: Локализация
        to=DicObjectColumn,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
    )

    class Meta:
        db_table = "meta\".\"dic_relationship"
