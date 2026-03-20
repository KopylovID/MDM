from django.db import models


class IDMixin:
    """Идентификатор записи"""

    id: models.IntegerField(
        verbose_name="Идентификатор записи",  # TODO: Локализация
    )
