from django.db import models


class UpdatedByMixin:
    """Пользователь обновивший запись"""

    updated_by = models.CharField(
        verbose_name="Пользователь обновивший запись",  # TODO: Локализация
    )
