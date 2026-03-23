from .base import BaseEntity
from django.db import models


class DicObject(BaseEntity):
    """Таблица объектов"""

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

    schema_name = models.CharField(
        verbose_name="Схема объекта БД",  # TODO: Локализация
        max_length=255,
    )

    object_name = models.CharField(
        verbose_name="Имя объекта  БД",  # TODO: Локализация
        max_length=255,
    )

    object_type = models.CharField(
        verbose_name="Тип объекта  БД",  # TODO: Локализация
        max_length=255,
        choices=[
            ("VIEW", "Представление"),  # TODO: Локализация
            ("TABLE", "Таблица"),  # TODO: Локализация
        ],
        default="TABLE"
    )

    class Meta:
        db_table = "dic_object"
