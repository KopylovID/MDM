from django.db import models
from django.conf import settings


class UpdatedByMixin(models.Model):
    """Пользователь обновивший запись"""

    updated_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Пользователь обновивший запись",  # TODO: Локализация
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, "_current_user"):
            self.updated_by = self._current_user
        super().save(*args, **kwargs)
