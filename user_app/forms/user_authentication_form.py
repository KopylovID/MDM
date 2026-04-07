from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UAAuthenticationForm(AuthenticationForm):
    """Форма для входа по email и паролю."""

    username = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите Email",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "••••••••",
        }),
    )

    def clean_email(self):
        username = self.cleaned_data.get("username").lower()
        return username
