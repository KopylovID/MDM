from base import BaseEntity
from django.db import models
from meta_app.models.dic_object import DicObject


class DicObjectRegister(BaseEntity):
    """Реестр зарегистрированных справочников"""

    dictionary_id = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        related_name="register",
        unique=True,
    )

    class Meta:
        db_table = "dic_object_register"
