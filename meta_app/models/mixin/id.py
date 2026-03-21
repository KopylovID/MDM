from django.db import models


class IDMixin:
    """Идентификатор записи"""

    id = models.AutoField(
        verbose_name="Идентификатор записи",  # TODO: Локализация
        primary_key=True
    )
