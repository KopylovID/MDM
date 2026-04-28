from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dynamic_tables_app.services import DynamicTableService

class DTADynModelListView(LoginRequiredMixin, ListView):
    """Список динамических моделей"""

    template_name = "dynamic_tables_app/dyn_model_list_view.html"
    context_object_name = "dyn_model_list"

    def get_head_data(self):
        return {"title": "Список динамических моделей"}

    def get_queryset(self, **kwargs):

        queryset = DynamicTableService.list_tables()

        # Фильтрация по ролям
        if self.request.user.groups.filter(name="Архитектор").exists():
            return queryset
        else:
            return queryset.none()  # Доступ запрещён