from django.db import models


class CreatedByMixin:
    """Пользователь создавший запись"""

    created_by: models.CharField(
        verbose_name="Пользователь создавший запись",  # TODO: Локализация
    )
