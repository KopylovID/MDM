from django.views import View
from dynamic_tables_app.forms import DTARecordUpdateForm
from django.shortcuts import render, redirect
from dynamic_tables_app.services import DynamicTableService
from django.contrib import messages

class DynamicRecordUpdateView(View):

    def get(self, request, table_name, record_id):

        form = DTARecordUpdateForm(table_name=table_name, record_id=record_id)
        context = {
            'form': form,
            'table_name': table_name,
            'record_id': record_id,
            'action_text': f"Изменение записи для {table_name} - {record_id}",
            'head': {"title": "Редактирование записи"},

        }
        return render(request, "dynamic_tables_app/dyn_model_record_modify.html", context=context)

    def post(self, request, table_name, record_id):
        form = DTARecordUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("data")
            count = DynamicTableService.update_record(table_name, record_id, data)

            if count == 0:
                messages.warning(request, f'Запись {record_id} не найдена')
            else:
                messages.success(request, f'Запись с ИД {record_id} изменена')
            return redirect('dta:get_table_data', table_name=table_name)
        return redirect('dta:get_table_data', table_name=table_name)