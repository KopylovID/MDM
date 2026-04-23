from core.models.base import BaseEntity
from django.db import models
from ..models import Object
from django.conf import settings

# TODO: На данный момент пока согласование сделаем одной таблицей, хотя по факту надо привести к нормальной форме

class ObjectRegistration(BaseEntity):
    """Таблица регистрации объектов"""

    dictionary = models.OneToOneField(
        verbose_name="Идентификатор справочника",  # TODO: Локализация
        to=Object,
        on_delete=models.CASCADE,
        related_name="registrations",
        db_index=False,
    )

    is_approve = models.BooleanField(
        verbose_name="Согласование",  # TODO: Локализация
        null=True,
        blank=True,
    )

    approve_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Пользователь согласовавший справочник",  # TODO: Локализация
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_approved",
        editable=False,
    )

    approve_at = models.DateTimeField(
        verbose_name="Дата и время согласования",  # TODO: Локализация
        blank=True,
        auto_now_add=True,
    )

    class Meta:
        db_table = '"meta_app"."object_registration"'

    def save(self, *args, **kwargs):
        if hasattr(self, "_current_user"):
            self.approve_by = self._current_user
        super().save(*args, **kwargs)
