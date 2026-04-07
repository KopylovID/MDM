from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from ..forms import UAAuthenticationForm


class UALoginView(LoginView):
    template_name = 'user_app/login.html'
    authentication_form = UAAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('ma:index')