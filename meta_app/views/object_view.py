from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from ..models import Object, ObjectRegistration
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        pk = kwargs.get('instance').pk
        is_reg = ObjectRegistration.objects.filter(dictionary_id=pk).values('is_approve').first().get('is_approve', False)

        kwargs['is_reg'] = is_reg

        return kwargs



class MAObjectDeleteView(ObjectBase, DeleteView):
    """Представления для удаления объекта."""

    template_name = "meta_app/object_delete.html"
    form_class = MAObjectDeleteForm
    success_url = reverse_lazy("ma:index")
