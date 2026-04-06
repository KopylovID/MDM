from core.models.base import BaseEntity
from django.db import models
from meta_app.models.object import Object
from meta_app.models.structure import Structure


class ObjectStructureLink(BaseEntity):
    """Привязка справочника к дереву"""

    dictionary = models.ForeignKey(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=Object,
        on_delete=models.CASCADE,
        related_name="dictonary",
        db_index=False,
    )

    structure = models.ForeignKey(
        verbose_name="Идентификатор структуры",  # TODO: Локализация
        to=Structure,
        on_delete=models.CASCADE,
        related_name="structure",
        db_index=False,
    )

    class Meta:
        db_table = '"meta_app"."object_structure_link"'

        constraints = [
            models.UniqueConstraint(fields=["dictionary_id", "structure_id"], name="UQ_dictionary_structure")
        ]
