from django.views.generic import ListView
from ..models import Object, ObjectRegistration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q


class MARegObjectView(LoginRequiredMixin, ListView):
    """Главная страница"""

    template_name = "meta_app/objects.html"
    model = Object
    context_object_name = "dict_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = {"title": "Список зарегистрированных справочников"}
        context['is_reg'] = True

        user = self.request.user

        # Проверяем конкретные группы
        context['is_arch'] = user.groups.filter(name='Архитектор').exists()
        context['is_user'] = user.groups.filter(name='Пользователь').exists()


        return context

    def get_queryset(self, **kwargs):

        if self.request.user.groups.filter(name="Архитектор").exists():
            queryset = (
                Object.objects.defer("id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at")
                .filter(registrations__is_approve=True)
                .all()
                .order_by("-created_at")
            )

            return queryset
        else:
            queryset = (
                Object.objects.defer("id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at", "created_by")
                .filter(created_by=self.request.user, registrations__is_approve=True)
                .all()
                .order_by("-created_at")
            )

            return queryset