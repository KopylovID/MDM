from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.views.generic import ListView

from ..models import Object, ObjectRegistration


class MAIndexView(LoginRequiredMixin, ListView):
    """Главная страница"""

    template_name = "meta_app/index.html"
    model = Object
    context_object_name = "dict_list"

    def get_head_data(self):
        return {"title": "Главная страница"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = self.get_head_data()

        user = self.request.user

        # Проверяем конкретные группы
        context["is_arch"] = user.groups.filter(name="Архитектор").exists()
        context["is_user"] = user.groups.filter(name="Пользователь").exists()
        context['search_query'] = self.request.GET.get('q', '')

        return context

    def get_queryset(self, **kwargs):

        queryset = (
            Object.objects.only("id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at")
            .prefetch_related(
                Prefetch(
                    "registrations",
                    queryset=ObjectRegistration.objects.only("dictionary", "is_approve", "id"),
                )
            )
            .order_by("-created_at")
        )

        # Получаем поисковый запрос
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(dic_code__icontains=search_query) |
                Q(dic_name__icontains=search_query) |
                Q(object_name__icontains=search_query)
            )

        # Фильтрация по ролям
        if self.request.user.groups.filter(name="Архитектор").exists():
            return queryset  # Архитектор видит всё
        elif self.request.user.groups.filter(name="Пользователь").exists():
            return queryset.filter(created_by=self.request.user)  # Только свои
        else:
            return queryset.none()  # Доступ запрещён
