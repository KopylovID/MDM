from django.views.generic import CreateView
from ..models import Object
from ..forms import ObjectAddModelForm
from django.urls import reverse_lazy
from django.contrib import messages


class MAObjectCreateView(CreateView):
    model = Object
    template_name = "meta_app/object_add.html"
    form_class = ObjectAddModelForm
    success_url = reverse_lazy("ma:index")

    def form_valid(self, form):
        messages.success(self.request, "Объект успешно добавлен")
        return super().form_valid(form)
