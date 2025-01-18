from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm

from config.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("phone", "first_name", "last_name", "email")

class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", 'avatar', 'email', "description", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class UserResetPasswordForm(StyleFormMixin,PasswordResetForm):
    pass

class UserResetPasswordConfirmForm(StyleFormMixin, SetPasswordForm):
    pass