import datetime

import stripe
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import image_verify, NoImageException, handle_uploaded_file

from config import settings
from config.settings import STRIPE_WEBHOOK
from config.special_elements import PRICE_MONTH, PRICE_6_MONTH, PRICE_YEAR
from profitpages.forms import PublicationForm, PublisherForm
from profitpages.models import Publisher, Publication, Subscription
from profitpages.services import new_create_stripe_session
from users.models import User, Payment


class PublicationListView(ListView):
    model = Publication
    template_name = "profitpages/home.html"
    context_object_name = "publications"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home Page"
        return context


class PublicationCreateView(CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = "profitpages/publication_form.html"
    success_url = reverse_lazy('profitpages:main')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PublicationDetailView(DetailView):
    model = Publication

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class PublicationUpdateView(UpdateView):
    model = Publication
    form_class = PublicationForm

    def get_success_url(self):
        return reverse_lazy('profitpages:publication_detail', args=[self.object.id])

    # def get_object(self, queryset=None):
    #     obj = super().get_object()
    #     if obj.owner != self.request.user:
    #         raise Http404(_("Разрешено изменять только свои публикации"))
    #     return obj


class PublicationDeleteView(DeleteView):
    model = Publication

    def get_success_url(self):
        return reverse_lazy('profitpages:main')


class PublicationAuthorlistView(ListView):
    context_object_name = 'publications'
    template_name = "profitpages/home.html"
    paginate_by = 5

    def get_queryset(self):
        author_id = self.kwargs.get('pk')
        author = get_object_or_404(Publisher, pk=author_id)
        return Publication.objects.filter(publisher=author).order_by('-updated_at')


class PublisherListView(ListView):
    model = Publisher
    context_object_name = "publishers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "List of Publishers"
        return context


class PublisherCreateView(CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = "profitpages/publisher_form.html"
    success_url = reverse_lazy('profitpages:main')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class PublisherDetailView(DetailView):
    model = Publisher
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PublisherUpdateView(UpdateView):
    model = Publisher
    form_class = PublisherForm

    def get_success_url(self):
        return reverse_lazy('profitpages:publisher_detail', args=[self.object.id])




class PublisherDeleteView(DeleteView):
    model = Publisher
    def get_success_url(self):
        return reverse_lazy('profitpages:main')


def upload_file(request):
    """
    Переписанная функция из .venv/lib/site-packages/django_ckeditor_5/view.py
    Библиотека запрещает загружать файлы, если user.is_staff=False
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        allow_all_file_types = getattr(settings, "CKEDITOR_5_ALLOW_ALL_FILE_TYPES", False)

        if not allow_all_file_types:
            try:
                image_verify(request.FILES['upload'])
            except NoImageException as ex:
                return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        if form.is_valid():
            url = handle_uploaded_file(request.FILES["upload"])
            return JsonResponse({"url": url})
    raise Http404(_("Page not found"))


def publication_set_paid(request, pk):
    """
    Переключение типа подписки (платная/бесплатная)
    """
    publication = get_object_or_404(Publication, pk=pk)
    if publication.paid:
        publication.paid = False
    else:
        publication.paid = True
    publication.save()
    return redirect(reverse('profitpages:main'))



def buy_subscription(request):
    """
    Покупка подписки
    """
    price_month = PRICE_MONTH
    price_6_month = PRICE_6_MONTH
    price_year = PRICE_YEAR

    total_price_6_month = price_6_month * 6
    total_price_year = price_year * 12

    id_session_month, url_month = new_create_stripe_session(price_month)
    Payment.objects.create(
        user=request.user,
        session_id=id_session_month,
        price=price_month,
    )
    id_session_6_month, url_6_month = new_create_stripe_session(total_price_6_month)
    Payment.objects.create(
        user=request.user,
        session_id=id_session_6_month,
        price=total_price_6_month,
    )
    id_session_year, url_year = new_create_stripe_session(total_price_year)
    Payment.objects.create(
        user=request.user,
        session_id=id_session_year,
        price=total_price_year,
    )

    context = {
        'price_month': price_month,
        'price_6_month': price_6_month,
        'price_year': price_year,

        'total_price_6_month': total_price_6_month,
        'total_price_year': total_price_year,

        'url_month': url_month,
        'url_6_month': url_6_month,
        'url_year': url_year,

    }
    return render(request, 'profitpages/subscription_create.html', context)

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, signature_header, STRIPE_WEBHOOK)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment = Payment.objects.get(session_id=session['id'])
        payment.is_paid = True
        payment.paid_at = timezone.now()
        payment.save()
        payments_list_to_remove = Payment.objects.filter(user=payment.user).filter(is_paid=False)
        for payment_to_remove in payments_list_to_remove:
            payment_to_remove.delete()

        if int(session['amount_total']) == PRICE_MONTH * 100:
            end_time = timezone.now() + datetime.timedelta(days=30)
        elif int(session['amount_total']) == PRICE_6_MONTH * 6 * 100:
            end_time = timezone.now() + datetime.timedelta(days=180)
        elif int(session['amount_total']) == PRICE_YEAR * 12 * 100:
            end_time = timezone.now() + datetime.timedelta(days=365)
        else:
            end_time = 'session["amount_total"] =! any of [PRICE_MONTH, PRICE_6_MONTH, PRICE_YEAR]'

        Subscription.objects.create(
            user=payment.user,
            is_active=True,
            update_at=timezone.now(),
            end_at=end_time
        )
        user = User.objects.get(['pk'])
        user.is_subscribed = True
        user.save()

    return HttpResponse(status=200)



