from base import BaseEntity
from django.db import models
from dic_object import DicObject
from dic_attr_type import DicAttrType

class DicObjectAttr(BaseEntity):
    """Класс атрибуттов справочника"""

    dictionary_id = models.ForeignObject(
        verbose_name="Дата и время обновления объекта",  # TODO: Локализация
        to=DicObject,
        related_name='attributes'
    )

    attr_name = models.CharField(
        verbose_name="Наименование атрибута",  # TODO: Локализация
        max_length=255
    )

    attr_description = models.TextField(
        verbose_name="Детальное описание атрибута",  # TODO: Локализация
    )

    attr_type_id = models.ForeignObject(
        verbose_name="Тип атрибута",  # TODO: Локализация
        to=DicAttrType,
        related_name='+', # Отключаем обратное обращение
        related_query_name='+', # Отключаем фильтрацию
    )

    class Meta:
        db_table = "dic_object_attr"