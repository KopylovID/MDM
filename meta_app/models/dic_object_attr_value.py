from django.db import models
from .dic_object import DicObject
from .dic_object_attr import DicObjectAttr
from .base import BaseEntity


class PrValueMixin(models.Model):

    @property
    def value(self):
        if hasattr(self, "value"):
            return self.value
        return None

    class Meta:
        abstract = True  # Не создаем модель


class BaseDicObjectAttrValue(BaseEntity, PrValueMixin):
    """Базовый класс значений атрибутов справочника"""

    dictionary_id = models.ForeignKey(
        verbose_name="Идентификатор справочника", # TODO: Локализация
        to=DicObject,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_attributes",
    )

    attribute_id = models.ForeignKey(
        verbose_name="Идентификатор атрибута справочника",  # TODO: Локализация
        to=DicObjectAttr,
        on_delete=models.CASCADE,
        related_name="+",  # Отключаем обратное обращение
        related_query_name="+",  # Отключаем фильтрацию
    )

    class Meta:
        abstract = True  # Не создаем модель


class DicObjectAttrValueInt(BaseDicObjectAttrValue):
    """Класс целых значений атрибутов справочника"""

    value = models.IntegerField(
        verbose_name="Значение атрибута",  # TODO: Локализация
    )

    class Meta:
        db_table = "dic_object_attr_value_int"


class DicObjectAttrValueNumeric(BaseDicObjectAttrValue):
    """Класс целых значений атрибутов справочника"""

    value = models.IntegerField(
        verbose_name="Значение атрибута",  # TODO: Локализация
    )

    class Meta:
        db_table = "dic_object_attr_value_numeric"


class DicObjectAttrValueStr(BaseDicObjectAttrValue):
    """Класс строковых значений атрибутов справочника"""

    value = models.TextField(
        verbose_name="Значение атрибута",  # TODO: Локализация
    )

    class Meta:
        db_table = "dic_object_attr_value_str"


class DicObjectAttrValueJson(BaseDicObjectAttrValue):
    """Класс json значений атрибутов справочника"""

    value = models.TextField(
        verbose_name="Значение атрибута",  # TODO: Локализация
    )

    class Meta:
        db_table = "dic_object_attr_value_json"


# TODO: Необходима реализация общего класса DicObjectAttrValue():
# TODO: Необходима реализация дополнительного класса содержащего значения справочника по умолчанию:
