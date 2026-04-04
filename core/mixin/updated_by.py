from django.db import models


class UpdatedByMixin(models.Model):
    """Пользователь обновивший запись"""

    updated_by = models.CharField(
        verbose_name="Пользователь обновивший запись",  # TODO: Локализация
        null=True
    )

    class Meta:
        abstract = True