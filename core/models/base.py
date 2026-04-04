from django.db import models
from django_dto import DTOMixin
from dataclasses import dataclass, asdict
import operator
from typing import Literal, Dict

from core.mixin import IDMixin, CreatedAtMixin, CreatedByMixin, UpdatedByMixin, UpdatedAtMixin, UUIDMixin


class BaseEntity(
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin,
    models.Model,
    DTOMixin,
):
    """Базовый класс для создания основых сущностей"""

    class Meta:
        abstract = True  # Не создаем модель


@dataclass
class BaseDTO:

    __model__: models.Model

    def get_fields(self, filter: Literal["all", "unique", "non-unique"] = "all") -> Dict:
        """Возвращает словарь необходимыми полями"""

        unique_fields = []
        for field in self.__model__._meta.fields:
            if hasattr(field, "unique") and field.unique:
                unique_fields.append(field.name)

        action = {
            "unique": lambda x, y: operator.contains(x, y),
            "non-unique": lambda x, y: operator.not_(operator.contains(x, y)),
            "all": lambda: True,
        }

        return {key: val for key, val in self.to_dict().items() if action[filter](unique_fields, key)}

    def to_dict(self) -> Dict:
        """Возвращает словарь только поля, которые не попадают под шаблон __<название поля>__"""
        return {key: val for key, val in asdict(self).items() if not (key.startswith("__") and key.endswith("__"))}
