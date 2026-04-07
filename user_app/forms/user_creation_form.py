from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UACreationForm(UserCreationForm):
    """Форма для регистрации нового пользователя на основе стандартной модели."""

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"},  # TODO: Локализация
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "staff_code",
            "user_name",
            "first_name",
            "last_name",
            "middle_name",
        )

    def clean_email(self):
        """Проверка email на уникальность."""

        email = self.cleaned_data.get("email").lower()
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")  # TODO: Локализация
        return email
