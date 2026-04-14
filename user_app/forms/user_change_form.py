from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class UAChangeForm(UserChangeForm):
    password = None  # Убираем поле пароль из формы

    staff_code = forms.CharField(
        required=True,
        label="Табельный номер",  # TODO: Локализация
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "000000"},  # TODO: Локализация
        ),
    )

    first_name = forms.CharField(
        required=True,
        label="Имя",  # TODO: Локализация
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Иван"},  # TODO: Локализация
        ),
    )
    last_name = forms.CharField(
        required=True,
        label="Фамилия",  # TODO: Локализация
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Иванов"},  # TODO: Локализация
        ),
    )
    middle_name = forms.CharField(
        required=False,
        label="Отчество",  # TODO: Локализация
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Иванович"},  # TODO: Локализация
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "staff_code",
            "first_name",
            "last_name",
            "middle_name",
        )

    # TODO: Дублирование кода


    def clean_staff_code(self):
        """Проверка табельного номера."""
        staff_code = self.cleaned_data.get("staff_code")

        if not staff_code.isdigit():
            raise forms.ValidationError("Табельный номер должен содержать только цифры") # TODO: Локализация
        if len(staff_code) != 6:
            raise forms.ValidationError("Табельный номер должен содержать 6 цифр") # TODO: Локализация
        return staff_code