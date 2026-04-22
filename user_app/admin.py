from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_app.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "staff_code", "first_name", "last_name")

    # Поля, которые будут в форме создания/редактирования
    fieldsets = (
        (
            "Обязательная информация",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "staff_code",
                )
            },
        ),
        (
            "Пароль",
            {"fields": ("password",), "classes": ("wide",)},
        ),
        (
            "Дополнительная информация (необязательно)",
            {"fields": ("middle_name",), "classes": ("collapse",)},  # сворачиваемая секция
        ),
        (
            "Группы",
            {"fields": ("groups",)},
        ),
    )

    add_fieldsets = (
        (
            "Обязательная информация",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "staff_code",
                    "password1",
                    "password2",
                ),  # Только email и пароль
            },
        ),
        (
            "Дополнительная информация (необязательно)",
            {"fields": ("middle_name",), "classes": ("collapse",)},  # сворачиваемая секция
        ),
        (
            "Группы",
            {"fields": ("groups",)},
        ),
    )

    ordering = ("email",)
