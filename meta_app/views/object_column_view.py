from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from ..models import ObjectColumn, Object
from ..forms import (
    MAObjectColumnModifyModelForm,
    MAObjectColumnDeleteForm,
)
from django.urls import reverse_lazy
from .mixin import SaveCreatedByMixin, SaveUpdatedByMixin


class ObjectColumnBase:
    model = ObjectColumn


class DictionaryIdFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["dictionary_id"] = self.kwargs.get("dictionary_id")
        return kwargs

class MAObjectColumnListView(ObjectColumnBase, ListView):
    """Представления списка колонок"""

    template_name = "meta_app/object_column.html"
    context_object_name = "col_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["head"] = {"title": "Главная страница"}
        context["dictionary_id"] = self.kwargs.get("dictionary_id")

        dic_object = Object.objects.get(id=context["dictionary_id"])
        context["object_name"] = (
            f"{dic_object.dic_code} - {dic_object.dic_name} ({dic_object.schema_name}.{dic_object.object_name})"
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        dictionary_id = self.kwargs.get("dictionary_id")

        if dictionary_id:
            queryset = queryset.filter(dictionary_id=dictionary_id).select_related("dictionary")

        return queryset.order_by("ordinal_position")


class MAObjectColumnCreateView(ObjectColumnBase, DictionaryIdFormMixin, SaveCreatedByMixin, CreateView):
    """Представления для добавления колонки объекта."""

    template_name = "meta_app/object_column_add.html"
    form_class = MAObjectColumnModifyModelForm

    def get_success_url(self):
        return reverse_lazy("ma:object_column", kwargs={"dictionary_id": self.kwargs.get("dictionary_id")})


class MAObjectColumnUpdateView(ObjectColumnBase, DictionaryIdFormMixin, SaveUpdatedByMixin, UpdateView):
    """Представления для редактирования колонки объекта."""

    template_name = "meta_app/object_column_edit.html"
    form_class = MAObjectColumnModifyModelForm

    def get_success_url(self):
        return reverse_lazy("ma:object_column", kwargs={"dictionary_id": self.kwargs.get("dictionary_id")})

class MAObjectColumnDeleteView(ObjectColumnBase, DeleteView):
    """Представления для удаления колонки объекта."""

    template_name = "meta_app/object_column_delete.html"
    form_class = MAObjectColumnDeleteForm

    def get_success_url(self):
        return reverse_lazy("ma:object_column", kwargs={"dictionary_id": self.kwargs.get("dictionary_id")})