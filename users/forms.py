from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    pass


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone", "first_name", "last_name", "email")
