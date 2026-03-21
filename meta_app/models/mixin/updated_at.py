from django.db import models


class UpdatedAtMixin:
    """Дата и время обновления объекта"""

    updated_at = models.DateTimeField(
        verbose_name="Дата и время обновления объекта",  # TODO: Локализация
        auto_now=True
    )
