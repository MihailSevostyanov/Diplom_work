from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from config.settings import DEBUG
from profitpages.services import send_sms
from users.forms import UserLoginForm, UserRegisterForm

User = get_user_model()


class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy("users:login")
    pass


class UserLoginView(LoginView):
    form_class = UserLoginForm


class SMSVerificationView(View):
    def post(self, request):
        submitted_sms = request.POST.get("sms")
        saved_sms = request.session.get("sms")

        password = request.session.get("password")
        email = request.session.get("email")
        first_name = request.session.get("first_name")
        last_name = request.session.get("last_name")

        if submitted_sms == saved_sms:
            phone = request.session.get("phone")
            User = get_user_model()
            user = User.objects.create(
                phone=phone,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()
            return redirect("users:login")
        else:
            messages.error(request, "Смс не верифицирован!")
            return render(
                request,
                "users/register.html",
                {"form": UserRegisterForm(request.POST), "sms_required": True},
            )


class RegisterView(CreateView):
    def get(self, request, **kwargs):
        if request.session.get("sms"):
            form = UserRegisterForm()
        else:
            form = UserRegisterForm()
        return render(
            request, "users/register.html", {"form": form, "sms_required": False}
        )

    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data["phone"])
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            if "sms" in request.POST:
                return SMSVerificationView.as_view()(request)
            else:
                password = form.cleaned_data["password1"]
                if not DEBUG:
                    sms = str(send_sms(phone))
                    print(f"Ваш код подтверждения: {sms}")
                else:
                    sms = "1234"

                request.session["sms"] = sms
                request.session["phone"] = phone
                request.session["password1"] = password
                request.session["email"] = email
                request.session["first_name"] = first_name
                request.session["last_name"] = last_name
                form.fields["password1"].widget.attrs["value"] = password
                form.fields["password2"].widget.attrs["value"] = password

                return render(
                    request, "users/register.html", {"form": form, "sms_required": True}
                )
        return render(
            request, "users/register.html", {"form": form, "sms_required": True}
        )


def payment_success(request):
    return render(request, 'users/payment_success.html')

def payment_cancel(request):
    return render(request, 'users/payment_cancel.html')