from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Управляет созданием обычного и суперпользователя."""

    def create_user(self, email, password, **extra_fields):
        """Создает обычного пользователя с email и паролем."""

        if not email:
            raise ValueError('Поле "email" - обязательно к заполнению!')  # TODO: Локализация

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создает суперпользователя."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                'Для суперпользователя признак "is_staff" - возможность войти в административную панель, является обязательным!'
            )  # TODO: Локализация

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                'Для суперпользователя признак "is_superuser" - признак суперпользователя, является обязательным!'
            )  # TODO: Локализация

        return self.create_user(email, password, **extra_fields)
