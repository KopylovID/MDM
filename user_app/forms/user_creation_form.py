from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model


class UACreationForm(BaseUserCreationForm):
    """Форма для регистрации нового пользователя на основе стандартной модели."""

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"},  # TODO: Локализация
        ),
    )

    staff_code = forms.CharField(
        required=True,
        label="Табельный номер",  # TODO: Локализация
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "000000"},  # TODO: Локализация
        ),
    )

    first_name = forms.CharField(
        required=True,
        label="Имя",  # TODO: Локализация
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Иван"},  # TODO: Локализация
        ),
    )
    last_name = forms.CharField(
        required=True,
        label="Фамилия",  # TODO: Локализация
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Иванов"},  # TODO: Локализация
        ),
    )
    middle_name = forms.CharField(
        required=False,
        label="Отчество",  # TODO: Локализация
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Иванович"},  # TODO: Локализация
        ),
    )

    password1 = forms.CharField(
        label="Пароль", # TODO: Локализация
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
                "autocomplete": "new-password"
            }
        ),
        help_text="Пароль должен содержать минимум 8 символов", # TODO: Локализация
    )

    password2 = forms.CharField(
        label="Подтверждение пароля", # TODO: Локализация
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Повторите пароль",
                "autocomplete": "new-password"
            }
        ),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.", # TODO: Локализация
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "staff_code",
            "first_name",
            "last_name",
            "middle_name",
            "password1",
            "password2"
        )

    def clean_email(self):
        """Проверка email на уникальность."""

        email = self.cleaned_data.get("email").lower()
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")  # TODO: Локализация
        return email


    def clean_staff_code(self):
        """Проверка табельного номера."""
        staff_code = self.cleaned_data.get("staff_code")

        if not staff_code.isdigit():
            raise forms.ValidationError("Табельный номер должен содержать только цифры")
        if len(staff_code) != 6:
            raise forms.ValidationError("Табельный номер должен содержать 6 цифр")
        return staff_code
