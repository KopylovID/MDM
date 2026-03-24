from django.db import models
from django_dto import DTOMixin

from .mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin
)


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