from django.db import models
from .mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin
)


class BaseEntity(
    models.Model,
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin,
):
    """Базовый класс для создания основых сущностей"""

    class Meta:
        abstract = False  # Не создаем модель