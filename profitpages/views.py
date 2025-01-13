from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import image_verify, NoImageException, handle_uploaded_file

from config import settings
from profitpages.forms import PublicationForm
from profitpages.models import Publisher, Content


class PublicationListView(ListView):
    model = Content
    template_name = "profitpages/home.html"
    context_object_name = "publications"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home Page"
        return context

class PublicationCreateView(CreateView):
    model = Content
    form_class = PublicationForm
    template_name = "profitpages/content_form.html"
    success_url = reverse_lazy('profitpages:main')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PublisherListView(ListView):
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "List of Publishers"
        return context


class PublisherCreateView(CreateView):
    pass


class PublisherUpdateView(UpdateView):
    pass


class PublisherDeleteView(DeleteView):
    pass


def upload_file(request):
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


