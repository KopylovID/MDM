from django.db import models


class UUIDMixin:
    """Уникальный Идентификатор записи"""

    uuid = models.UUIDField(
        verbose_name="Уникальный идентификатор записи",  # TODO: Локализация
        unique=True
    )
