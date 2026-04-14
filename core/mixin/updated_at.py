from django.db import models


class UpdatedAtMixin(models.Model):
    """Дата и время обновления объекта"""

    updated_at = models.DateTimeField(
        verbose_name="Дата и время обновления объекта",  # TODO: Локализация
        blank=True,
        auto_now=True,
        null=True
    )

    class Meta:
        abstract = True