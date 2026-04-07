from django.views.generic.base import TemplateView


class MAIndexView(TemplateView):
    """Главная страница"""

    template_name = "meta_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = {"title": "Главная страница"}
        return context
