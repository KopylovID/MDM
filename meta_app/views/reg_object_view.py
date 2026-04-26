import datetime
import logging

from django.contrib import messages
from django.db.models import F, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect

from ..models import Object, ObjectColumn, ObjectRegistration
from .index_view import MAIndexView
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def json_response(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={'ensure_ascii': False})

class MARegObjectView(MAIndexView):
    """Главная страница"""

    template_name = "meta_app/objects.html"
    # model = Object
    # context_object_name = "dict_list"

    def get_head_data(self):
        return {"title": "Список справочников в разработке"}

    def get_html_view_tag(self):
        return "reg_object"

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
                created_by=self.request.user,
                created_at=datetime.datetime.now()
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
                from dynamic_tables_app.services import DynamicTableService

                obj_reg.is_approve = False
                obj_reg.approve_by = self.request.user
                obj_reg.approve_at = datetime.datetime.now()
                obj_reg.save()
                if DynamicTableService.delete_table(obj_reg.dictionary.object_name):
                    messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" снят с регистрации')
                else:
                    messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" не удалось снять с регистрации')

            else:
                messages.success(
                    request,
                    f'Справочник "{obj_reg.dictionary.dic_name}" зарегистрирован! Отозвать согласование не удалось',
                )
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

        return redirect("ma:reg_object")

    def handle_approve(self, request, object_id):

        from dynamic_tables_app.services import DynamicTableService
        from meta_app.services import MACreateSchema

        try:
            obj_reg = get_object_or_404(ObjectRegistration, dictionary_id=object_id)
            obj_reg.is_approve = True
            obj_reg.approve_by = self.request.user
            obj_reg.approve_at = datetime.datetime.now()

            # Пример схемы
            # {
            #     'schema_name': 'public',
            #     'table_name': 'Product',
            #     'fields': [
            #         {'name': 'name', 'type': 'CharField', 'max_length': 200},
            #         {'name': 'price', 'type': 'DecimalField', 'max_digits': 10, 'decimal_places': 2},
            #     ]
            # }
            obj = get_object_or_404(Object, pk=object_id)

            column_info = list(
                ObjectColumn.objects.filter(dictionary_id=object_id)
                .annotate(
                    name=F("column_name"),
                    type=F("column_type__tech_type_name"),
                    type_params=F("column_type__type_params"),
                )
                .values(
                    "is_null",
                    "is_pk",
                    "name",
                    "type",
                    "type_params",
                )
            )

            for idx, field_data in enumerate(column_info):
                type_params = field_data.pop('type_params')
                column_info[idx].update(dict() if type_params is None else type_params)
            schema = MACreateSchema.get_schema(schema_name=obj.schema_name, table_name=obj.object_name, fields=column_info)

            result = DynamicTableService.create_table(schema)
            messages.success(request, f"Таблица: {result.table_name} создана")

            obj_reg.save()
            messages.success(request, f'Справочник "{obj_reg.dictionary.dic_name}" Зарегистрирован')
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

        return redirect("ma:reg_object")


class MAToApproveObjectView(MARegObjectView):

    def get_html_view_tag(self):
        return "to_approve"

    def get_queryset(self, **kwargs):

        queryset = (
            Object.objects.only("id", "uuid", "dic_code", "dic_name", "schema_name", "object_name", "created_at")
            .filter(
                Q(registrations__id__isnull=False) & Q(registrations__is_approve__isnull=True)
                | Q(registrations__is_approve=False)
            )
            .prefetch_related(
                Prefetch(
                    "registrations",
                    queryset=ObjectRegistration.objects.only("dictionary", "is_approve", "id"),
                )
            )
            .order_by("-created_at")
        )

        # Получаем поисковый запрос
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(dic_code__icontains=search_query)
                | Q(dic_name__icontains=search_query)
                | Q(object_name__icontains=search_query)
            )

        # Фильтрация по ролям
        if self.request.user.groups.filter(name="Архитектор").exists():
            return queryset
        else:
            return queryset.none()  # Доступ запрещён
