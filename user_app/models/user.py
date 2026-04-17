from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from core.mixin import (
    CreatedAtMixin,
    UpdatedAtMixin,
    UUIDMixin,
)


class User(
    AbstractUser,
    CreatedAtMixin,
    UpdatedAtMixin,
    UUIDMixin,
):
    """Кастомный пользователь."""

    username = None  # Отключаем стандартное поле username в пользу user_name

    staff_code = models.CharField(
        verbose_name="Табельный номер",  # TODO: Локализация
        max_length=255,
        unique=False,
    )

    first_name = models.CharField(
        verbose_name="Имя",  # TODO: Локализация
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",  # TODO: Локализация
        max_length=150,
    )
    middle_name = models.CharField(
        verbose_name="Отчество",  # TODO: Локализация
        max_length=150,
        blank=True,
    )

    email = models.EmailField(
        verbose_name="Электронная почта",  # TODO: Локализация
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "staff_code",
        "first_name",
        "last_name",
        "middle_name",
    ]

    objects = UserManager()

    @property
    def user_name(self):
        """Вычисляемое имя пользователя"""
        name_parts = []

        if self.last_name:
            name_parts.append(self.last_name)
        if self.first_name:
            name_parts.append(self.first_name)
        if self.middle_name:
            name_parts.append(self.middle_name)

        return " ".join(name_parts)

    def get_full_name(self):
        return self.user_name

    class Meta:
        verbose_name = 'Пользователь' # TODO: Локализация
        verbose_name_plural = 'Пользователи' # TODO: Локализация
        db_table = '"user_app"."user"'
