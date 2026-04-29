from django import forms
from ..models import Object


class MAObjectModifyModelForm(forms.ModelForm):
    """Форма для добавления и редактирования объекта"""

    object_type = forms.ChoiceField(
        label="Тип объекта БД",
        choices=[
            ("VIEW", "Представление"),
            ("TABLE", "Таблица"),
        ],
        initial="TABLE",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Object
        fields = ("dic_code", "dic_name", "dic_description", "schema_name", "object_name", "object_type")
        widgets = {
            "dic_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите код справочника"}),
            "dic_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование справочника"}
            ),
            "dic_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "placeholder": "Введите расширенное описание справочника"}
            ),
            "schema_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите схему объекта в БД"}
            ),
            "object_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите наименование объекта в БД"}
            ),
            "object_type": forms.ChoiceField(
                label="Тип объекта БД",
                choices=[
                    ("VIEW", "Представление"),  # TODO: Локализация
                    ("TABLE", "Таблица"),  # TODO: Локализация
                ],
                initial="TABLE",
                widget=forms.Select(attrs={"class": "form-select"}),
            ),
        }

    def __init__(self, *args, **kwargs):
        self.is_reg = kwargs.pop('is_reg', False)
        super().__init__(*args, **kwargs)

        self.fields["schema_name"].initial = 'public'
        self.fields["schema_name"].disabled = True

        self.fields["object_type"].initial = 'TABLE'
        self.fields["object_type"].disabled = True

        if self.is_reg:
            self.disable_form_fields()

    def disable_form_fields(self):
        """Отключает все поля формы"""
        for field_name, field in self.fields.items():
            field.disabled = True


class MAObjectDeleteForm(forms.Form):
    """Форма для подтверждения удаления объекта"""

    confirm = forms.BooleanField(
        required=True,
        label="Подтверждение удаления",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
    )
