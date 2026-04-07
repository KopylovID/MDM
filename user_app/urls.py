from django.urls import path
from .views import UARegisterView, UALoginView, UALogoutView

app_name = 'ua'

urlpatterns = [
    path("register/", UARegisterView.as_view(), name="register"),
    path("login/", UALoginView.as_view(), name="login"),
    path("logout/", UALogoutView.as_view(), name="logout"),
]
