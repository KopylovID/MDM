from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login
from ..forms import UACreationForm


class UARegisterView(FormView):
    template_name = "user_app/register.html"
    form_class = UACreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
