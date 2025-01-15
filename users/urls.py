from django.contrib.auth.views import LogoutView
from django.urls import path, include

from users.apps import UsersConfig
from users.views import UserCreateView, UserLoginView, RegisterView, payment_success, payment_cancel

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(template_name="users/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
