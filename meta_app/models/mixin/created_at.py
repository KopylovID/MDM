from django.db import models


class CreatedAtMixin:
    """Дата и время создания объекта"""

    created_at: models.DateTimeField(
        verbose_name="Дата и время создания объекта",  # TODO: Локализация
        auto_now_add=True,
    )
