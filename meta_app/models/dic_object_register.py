from .base import BaseEntity
from django.db import models
from meta_app.models.dic_object import DicObject


class DicObjectRegister(BaseEntity):
    """Реестр зарегистрированных справочников"""

    dictionary = models.OneToOneField(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        on_delete=models.CASCADE,
        related_name="register",
        unique=True,
    )

    class Meta:
        db_table = "meta\".\"dic_object_register"
