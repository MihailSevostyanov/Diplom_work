from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from profitpages.models import Publisher, Content


class PublicationListView(ListView):
    model = Content
    template_name = "profitpages/home.html"
    context_object_name = "publications"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home Page"
        return context

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




