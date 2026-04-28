from django.views import View
from dynamic_tables_app.forms import DTARecordCreateForm
from django.shortcuts import render, redirect
from dynamic_tables_app.services import DynamicTableService
from django.contrib import messages

class DynamicRecordCreateView(View):

    def get(self, request, table_name):

        form = DTARecordCreateForm(table_name=table_name)
        context = {
            'form': form,
            'table_name': table_name,
            'action_text': f"Добавление записи для {table_name}",
            'head': {"title": "Создание записи"},

        }
        return render(request, "dynamic_tables_app/dyn_model_record_modify.html", context=context)

    def post(self, request, table_name):
        form = DTARecordCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("data")
            record = DynamicTableService.create_record(table_name, data)
            messages.success(request, f'Запись с ИД {record.get('id')} создана')
            return redirect('dta:get_table_data', table_name=table_name)

        context = {
            'form': form,
            'table_name': table_name,
            'head': {"title": "Список записей"},
        }
        return render(request, "dynamic_tables_app/dyn_model_record_modify.html", context=context)