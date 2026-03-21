from sequences import get_next_value
from django.db import models
from mixin import (
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUID
)


class BaseEntity(
    models.Model,
    IDMixin,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUID,
):
    """Базовый класс для создания основых сущностей"""

    class Meta:
        abstract = False  # Не создаем модель


    def save(self, *args, **kwargs):
        """Метод сохранения"""

        if not self.id:
            self.id = get_next_value("id")
        super().save(*args, **kwargs)
