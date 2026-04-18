from django import forms
from ..models import ObjectColumn


class MAObjectColumnModifyModelForm(forms.ModelForm):
    """Форма для добавления и редактирования колонок объекта"""

    is_null = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(),
        label="Обязательное",
    )

    is_pk = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(),
        label="Первичный ключ",
    )

    class Meta:
        model = ObjectColumn
        fields = (
            "dictionary",
            "column_name",
            "column_description",
            "column_type",
            "ordinal_position",
            "is_pk",
            "is_null",
        )
        widgets = {
            "dictionary": forms.Select(attrs={"class": "form-control"}),
            "column_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование столбца"}
            ),
            "column_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "placeholder": "Введите расширенное описание столбца"}
            ),
            "column_type": forms.Select(attrs={"class": "form-control"}),
            "ordinal_position": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        dictionary_id = kwargs.pop("dictionary_id", None)
        super().__init__(*args, **kwargs)

        if dictionary_id:
            self.fields["dictionary"].initial = dictionary_id
            self.fields["dictionary"].disabled = True


class MAObjectColumnDeleteForm(forms.Form):
    """Форма для подтверждения удаления колонки объекта"""

    confirm = forms.BooleanField(
        required=True,
        label="Подтверждение удаления",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
    )
