from importlib.resources._common import _

from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView, DetailView,
)
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import image_verify, NoImageException, handle_uploaded_file

from config import settings
from profitpages.forms import PublicationForm, PublisherForm
from profitpages.models import Publisher, Publication
from users.models import User


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
