from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserLoginView,
    SMSVerificationView, ProfileView, ProfileUpdateView, UserPasswordResetView, user_auto_generate_password,
    UserPasswordResetConfirmView, UserCreateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", cache_page(60)(UserLoginView.as_view(template_name="users/login.html")), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", cache_page(120)(UserCreateAPIView.as_view()), name="register"),
    path("verify-sms/", SMSVerificationView.as_view(), name="sms_verification"),

    path("profile/<int:pk>/", cache_page(10)(ProfileView.as_view()), name="profile"),
    path("profile/update/<int:pk>/", cache_page(10)(ProfileUpdateView.as_view()), name="profile_update"),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/auto-generate/done/', user_auto_generate_password, name='password_reset_auto_generate_done'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

]
