from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dynamic_tables_app.services import DynamicTableService

class DTADynModelRecordView(LoginRequiredMixin, ListView):
    """Список записей модели"""

    template_name = "dynamic_tables_app/dyn_model_record_view.html"
    context_object_name = "dyn_model_record"

    def get_queryset(self, **kwargs):
        table_name = self.kwargs.get("table_name")
        queryset = DynamicTableService.get_data(table_name)

        return list(queryset.values())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["head"] = {"title": "Список записей"}
        context["table_name"] = self.kwargs.get("table_name")

        data = context['dyn_model_record']
        if data and len(data) > 0:
            context['fields'] = list(data[0].keys())
        else:
            context['fields'] = []

        return context