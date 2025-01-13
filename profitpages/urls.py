from django.contrib import admin
from django.urls import path, include

from profitpages.apps import ProfitpagesConfig
from profitpages.views import (
    PublicationListView,
    PublisherListView,
    PublisherCreateView,
    PublisherUpdateView,
    PublisherDeleteView, PublicationCreateView,
)

app_name = ProfitpagesConfig.name


urlpatterns = [
    path("", PublicationListView.as_view(), name="main"),
    path("publication/create/", PublicationCreateView.as_view(), name="publication_create"),

    path("publisher/", PublisherListView.as_view(), name="publisher_list"),
    path("publisher/", PublisherCreateView.as_view(), name="publisher_create"),
    path(
        "publisher/update/<int:pk>",
        PublisherUpdateView.as_view(),
        name="publisher_update",
    ),
    path(
        "publisher/delete/<int:pk>",
        PublisherDeleteView.as_view(),
        name="publisher_delete",
    ),
]
