from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import (
    UserCreateView,
    UserLoginView,
    RegisterView,
    payment_success,
    payment_cancel,
    SMSVerificationView,
)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/", cache_page(60)(UserLoginView.as_view(template_name="users/login.html")), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", cache_page(120)(RegisterView.as_view()), name="register"),
    path("verify-sms/", SMSVerificationView.as_view(), name="sms_verification"),
]
