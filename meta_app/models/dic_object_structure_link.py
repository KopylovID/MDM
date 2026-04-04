from core.models.base import BaseEntity
from django.db import models
from meta_app.models.dic_object import DicObject
from meta_app.models.dic_structure import DicStructure


class DicObjectStructureLink(BaseEntity):
    """Привязка справочника к дереву"""

    dictionary = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=DicObject,
        on_delete=models.CASCADE,
        related_name="dictonary",
        db_index=False,
    )

    structure = models.ForeignKey(
        verbose_name="Идентификатор структуры",  # TODO: Локализация
        to=DicStructure,
        on_delete=models.CASCADE,
        related_name="structure",
        db_index=False,
    )

    class Meta:
        db_table = '"meta_app"."dic_object_structure_link"'

        constraints = [
            models.UniqueConstraint(fields=["dictionary_id", "structure_id"], name="UQ_dictionary_structure")
        ]
