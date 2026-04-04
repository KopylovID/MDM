from django.db import models


class CreatedByMixin(models.Model):
    """Пользователь создавший запись"""

    created_by = models.CharField(
        verbose_name="Пользователь создавший запись",  # TODO: Локализация
        default='', # TODO: Необходимо сделать сохранение текущего пользователя
    )

    class Meta:
        abstract = True