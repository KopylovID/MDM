from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from core.mixin import (
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin,
)


class DicUser(
    AbstractUser,
    CreatedAtMixin,
    CreatedByMixin,
    UpdatedByMixin,
    UpdatedAtMixin,
    UUIDMixin,
):
    """Кастомный пользователь."""

    username = None  # Отключаем стандартное поле username в пользу user_name

    staff_code = models.CharField(
        verbose_name="Имя пользователя",  # TODO: Локализация
        max_length=255,
        unique=False,
    )

    user_name = models.CharField(
        verbose_name="Имя пользователя",  # TODO: Локализация
        max_length=255,
        unique=False,
    )

    first_name = models.CharField(
        verbose_name="Имя",  # TODO: Локализация
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",  # TODO: Локализация
        max_length=150,
        blank=True,
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

    class Meta:
        db_table = '"user_app"."dic_user"'
