from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from config.settings import DEBUG
from profitpages.models import Subscription, Publication, Publisher
from profitpages.services import send_sms, send_auto_gen_password
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserResetPasswordForm, \
    UserResetPasswordConfirmForm
from users.models import User, Payment
from users.serializers import UserSerializer


class CustomLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")
    redirect_field_name = "redirect_to"


class UserLoginView(LoginView):
    form_class = UserLoginForm


class SMSVerificationView(View):
    def post(self, request):
        submitted_sms = request.POST.get("sms")
        saved_sms = request.session.get("sms")

        password = request.session.get("password1")
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


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

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
                if DEBUG:
                    sms = str(send_sms(phone))
                else:
                    sms = "1111"
                request.session["sms"] = sms
                request.session["phone"] = phone
                request.session["password1"] = password
                request.session["email"] = email
                request.session["first_name"] = first_name
                request.session["last_name"] = last_name
                form.fields["password1"].widget.attrs["value"] = password
                form.fields["password2"].widget.attrs["value"] = password
                print(
                    f"Спасибо за регистрацию на платформе ProfitPages!\n"
                    f"Ваш код подтверждения: {sms}"
                )

                return render(
                    request, "users/register.html", {"form": form, "sms_required": True}
                )
        return render(
            request, "users/register.html", {"form": form, "sms_required": False}
        )


class ProfileView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):

        try:
            if Subscription.objects.get(user=self.request.user):
                subscribe_hide = True
        except:
            subscribe_hide = False

        publisher = Publisher.objects.get(user=self.request.user)
        publications = Publication.objects.filter(publisher=publisher)
        last_publications = publications.order_by('-updated_at')[:2]

        context = super().get_context_data(**kwargs)
        context['publications'] = publications
        context['last_publications'] = last_publications
        context['subscribe_hide'] = subscribe_hide
        return context


class ProfileUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})


class UserPasswordResetView(PasswordResetView):
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('users:password_reset_done')
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserResetPasswordConfirmForm
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy('users:password_reset_complete')


def user_auto_generate_password(request):
    context = {
        "reset_message": "Новый пароль отправлен на почту"
    }
    if request.method == "POST":
        send_auto_gen_password(request, context)
    return render(request, "users/login.html", context)


def payment_success(request):
    user = request.user
    user.is_subscribed = True
    user.save()
    return render(request, "users/payment_success.html")


def payment_cancel(request):
    return render(request, "users/payment_cancel.html")
