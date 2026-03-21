from base import BaseEntity
from django.db import models

class DicAttrType(BaseEntity):

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
    )

    class Meta:
        db_table = 'dic_attr_type'