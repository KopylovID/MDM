from django.views.generic import ListView
from ..models import Object


class MAIndexView(ListView):
    """Главная страница"""

    template_name = "meta_app/index.html"
    model = Object
    context_object_name = "dict_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = {"title": "Главная страница"}
        return context

    def get_queryset(self, **kwargs):
        return (
            Object.objects.all().order_by("-created_at")
        )
