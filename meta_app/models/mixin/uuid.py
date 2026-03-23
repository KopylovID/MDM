from django.db import models
import uuid

class UUIDMixin:
    """Уникальный Идентификатор записи"""

    uuid = models.UUIDField(
        verbose_name="Уникальный идентификатор записи",  # TODO: Локализация
        unique=True,
        default=uuid.uuid4,  # автогенерация UUID
        editable=False,  # нельзя редактировать в админке
    )
