from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from ..models import Object
from ..forms import (
    MAObjectModifyModelForm,
    MAObjectDeleteForm,
)
from django.urls import reverse_lazy
from .mixin import SaveCreatedByMixin, SaveUpdatedByMixin


class ObjectBase:
    model = Object


class MAObjectCreateView(ObjectBase, SaveCreatedByMixin, CreateView):
    """Представления для добавления объекта."""

    template_name = "meta_app/object_add.html"
    form_class = MAObjectModifyModelForm
    success_url = reverse_lazy("ma:index")


class MAObjectUpdateView(ObjectBase, SaveUpdatedByMixin, UpdateView):
    """Представления для редактирвоания объекта."""

    template_name = "meta_app/object_edit.html"
    form_class = MAObjectModifyModelForm
    success_url = reverse_lazy("ma:index")


class MAObjectDeleteView(ObjectBase, DeleteView):
    """Представления для удаления объекта."""

    template_name = "meta_app/object_delete.html"
    form_class = MAObjectDeleteForm
    success_url = reverse_lazy("ma:index")
