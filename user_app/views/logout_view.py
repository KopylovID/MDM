from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView


class UALogoutView(LogoutView):
    next_page = reverse_lazy("login")
