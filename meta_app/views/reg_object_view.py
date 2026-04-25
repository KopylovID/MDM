import datetime

from ..models import Object, ObjectRegistration
from django.db.models import Prefetch, Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .index_view import MAIndexView


class MARegObjectView(MAIndexView):
    """Главная страница"""

    template_name = "meta_app/objects.html"
    # model = Object
    # context_object_name = "dict_list"

    def get_head_data(self):
        return {"title": "Список справочников в разработке"}

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        object_id = request.POST.get("dictionary_id")

        if action == "to_approve":
            return self.handle_to_approve(request, object_id)
        elif action == "revoke_approve":
            return self.handle_revoke_approve(request, object_id)
        elif action == "approve":
            return self.handle_approve(request, object_id)

        return redirect("ma:reg_object")

    def handle_to_approve(self, request, object_id):

        try:
            obj = get_object_or_404(Object, id=object_id)
            obj_reg, created = ObjectRegistration.objects.get_or_create(
                dictionary=obj,
            )
            if created:
                messages.success(request, f'Справочник "{obj.dic_name}" отправлен на согласование')
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

        return redirect("ma:reg_object")

    def handle_revoke_approve(self, request, object_id):

        is_arch = request.user.groups.filter(name="Архитектор").exists()

        try:
            obj_reg = get_object_or_404(ObjectRegistration, dictionary_id=object_id)
            if obj_reg.is_approve is None and obj_reg.is_approve != True:
                obj_reg.delete()
                messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" отозван из согласования')
            elif is_arch:
                obj_reg.is_approve = False
                obj_reg.approve_by = self.request.user
                obj_reg.approve_at = datetime.datetime.now()
                obj_reg.save()
                messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" снят с регистрации')
            else:
                messages.success(
                    request,
                    f'Справочник "{obj_reg.dictionary.dic_name}" зарегистрирован! Отозвать согласование не удалось',
                )
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

        return redirect("ma:reg_object")

    def handle_approve(self, request, object_id):

        try:
            obj_reg = get_object_or_404(ObjectRegistration, dictionary_id=object_id)
            obj_reg.is_approve = True
            obj_reg.approve_by = self.request.user
            obj_reg.approve_at = datetime.datetime.now()
            obj_reg.save()
            messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" Зарегистрирован')
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

        return redirect("ma:reg_object")


class MAToApproveObjectView(MARegObjectView):
    def get_queryset(self, **kwargs):

        queryset = (
            Object.objects.only("id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at")
            .filter(Q(registrations__id__isnull=False) & Q(registrations__is_approve__isnull=True) | Q(registrations__is_approve=False))
            .prefetch_related(
                Prefetch(
                    "registrations",
                    queryset=ObjectRegistration.objects.only(
                        "dictionary", "is_approve", "id"
                    ),
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
            return queryset
        else:
            return queryset.none()  # Доступ запрещён
