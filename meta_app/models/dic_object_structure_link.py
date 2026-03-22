from base import BaseEntity
from django.db import models
from meta_app.models.dic_object import DicObject


class DicObjectStructureLink(BaseEntity):
    """Привязка справочника к дереву"""

    dictionary_id = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        related_name="structure_tree",
        unique=True,
    )

    class Meta:
        db_table = "dic_object_structure_link"
