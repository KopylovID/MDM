from base import BaseEntity
from django.db import models


class DicObject(BaseEntity):
    """Объект справочника"""

    dic_code = models.CharField(
        verbose_name="Код объекта",  # TODO: Локализация
        max_length=255,
        unique=True,
    )
    dic_name = models.CharField(
        verbose_name="Наименование объекта",  # TODO: Локализация
        max_length=255,
    )
    dic_description = models.TextField(
        verbose_name="Детальное описание объекта",  # TODO: Локализация
    )

    class Meta:
        db_table = "dic_object"
