import datetime

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
                .filter(registrations__is_approve__isnull=True)
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
                .filter(created_by=self.request.user, registrations__is_approve__isnull=True)
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
        action = request.POST.get('action')
        object_id = request.POST.get('dictionary_id')

        if action == 'to_approve':
            return self.handle_to_approve(request, object_id)
        elif action == 'revoke_approve':
            return self.handle_revoke_approve(request, object_id)
        elif action == 'approve':
            return self.handle_approve(request, object_id)

        return redirect('ma:unreg_object')


    def handle_to_approve(self, request, object_id):

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

    def handle_revoke_approve(self, request, object_id):

        try:
            obj_reg = get_object_or_404(ObjectRegistration, dictionary_id=object_id)
            if obj_reg.is_approve is None and obj_reg.is_approve != True:
                obj_reg.delete()
                messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" отозван из согласования')
            elif obj_reg.is_approve == True:
                messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" зарегистрирован! Отозвать согласование не удалось')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

        return redirect('ma:unreg_object')

    def handle_approve(self, request, object_id):

        try:
            obj_reg = get_object_or_404(ObjectRegistration, dictionary_id=object_id)
            obj_reg.is_approve = True
            obj_reg.approve_by = self.request.user
            obj_reg.approve_at = datetime.datetime.now()
            obj_reg.save()
            messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" Зарегистрирован')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

        return redirect('ma:unreg_object')