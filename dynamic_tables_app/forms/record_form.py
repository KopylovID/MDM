from django import forms
import json
from meta_app.models import ObjectColumn
from django.db.models import F

class DTARecordCreateForm(forms.Form):
    """Форма для добавления"""

    def __init__(self, *args, **kwargs):
        self.table_name = kwargs.pop('table_name', None)
        super().__init__(*args, **kwargs)

        if self.table_name:
            self.fields['data'].label = f"Данные для таблицы {self.table_name}"

            column_info = list(
                ObjectColumn.objects.filter(dictionary__object_name=self.table_name)
                .annotate(
                    name=F("column_name")
                )
                .values("name")
            )
            result_data = { field_data.get('name'): "" for field_data in column_info}
            result_data.pop('id', None)

            placeholder_text = json.dumps(result_data, ensure_ascii=False)
            self.fields["data"].initial = placeholder_text

    data = forms.CharField(
        required=True,
        label="Данные (JSON)",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 10},
        ),
        help_text="Введите данные в формате JSON",
    )

    def clean_data(self):
        """Валидация JSON данных"""
        data = self.cleaned_data["data"]
        try:
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Неверный формат JSON: {e}")


class DTARecordUpdateForm(forms.Form):
    """Форма для редактирования"""

    def __init__(self, *args, **kwargs):
        self.table_name = kwargs.pop('table_name', None)
        self.record_id = kwargs.pop('record_id', None)
        super().__init__(*args, **kwargs)

        if self.table_name:
            from dynamic_tables_app.services import DynamicTableService

            self.fields['data'].label = f"Данные для таблицы {self.table_name}"
            data = DynamicTableService.get_data(self.table_name, filters={"id":self.record_id})

            result_data = list(data.values())[0]
            result_data.pop('id', None)

            placeholder_text = json.dumps(result_data, ensure_ascii=False)
            self.fields["data"].initial = placeholder_text

    data = forms.CharField(
        required=True,
        label="Данные (JSON)",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 10},
        ),
        help_text="Введите данные в формате JSON",
    )

    def clean_data(self):
        """Валидация JSON данных"""
        data = self.cleaned_data["data"]
        try:
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Неверный формат JSON: {e}")
