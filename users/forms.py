from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from config.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("phone", "first_name", "last_name", "email")
