from django.views import View
from django.shortcuts import redirect
from dynamic_tables_app.services import DynamicTableService
from django.contrib import messages

class DynamicRecordDeleteView(View):

    def post(self, request, table_name, record_id):
        count = DynamicTableService.delete_record(table_name, record_id)

        if count == 0:
            messages.warning(request, f'Запись {record_id} не найдена')
        else:
            messages.success(request, f'Запись с ИД {record_id} удалена')
        return redirect('dta:get_table_data', table_name=table_name)
