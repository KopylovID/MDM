from django.db import models
from datetime import datetime

class CreatedAtMixin(models.Model):
    """Дата и время создания объекта"""

    created_at = models.DateTimeField(
        verbose_name="Дата и время создания объекта",  # TODO: Локализация
        blank=True,
        auto_now_add=True,
    )

    class Meta:
        abstract = True