from django.views.generic import ListView
from ..models import Object, ObjectRegistration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages


class MAUnRegObjectView(LoginRequiredMixin, ListView):
    """Главная страница"""

    template_name = "meta_app/objects.html"
    model = Object
    context_object_name = "dict_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = {"title": "Список справочников в разработке"}
        context["is_reg"] = False

        user = self.request.user

        # Проверяем конкретные группы
        context["is_arch"] = user.groups.filter(name="Архитектор").exists()
        context["is_user"] = user.groups.filter(name="Пользователь").exists()

        return context


    def get_queryset(self, **kwargs):

        if self.request.user.groups.filter(name="Архитектор").exists():
            queryset = (
                Object.objects.only("id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at")
                .prefetch_related(
                    Prefetch(
                        "registrations",
                        queryset=ObjectRegistration.objects.filter(Q(is_approve=False) | Q(is_approve__isnull=True))
                        .only("dictionary", "is_approve", "id"),
                    )
                )
                .all()
                .order_by("-created_at")
            )

            return queryset
        else:
            queryset = (
                Object.objects.only(
                    "id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at", "created_by"
                )
                .filter(created_by=self.request.user)
                .prefetch_related(
                    Prefetch(
                        "registrations",
                        queryset=ObjectRegistration.objects.filter(Q(is_approve=False) | Q(is_approve__isnull=True))
                        .only("dictionary", "is_approve", "id"),
                    )
                )
                .all()
                .order_by("-created_at")
            )

            return queryset


    def post(self, request, *args, **kwargs):
        object_id = request.POST.get('dictionary_id')

        try:
            obj = get_object_or_404(Object, id=object_id)
            obj_reg, created = ObjectRegistration.objects.get_or_create(
                dictionary=obj,
            )
            if created:
                messages.success(request, f'Справочник "{obj.dic_name}" отправлен на согласование')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

        return redirect('ma:unreg_object')
