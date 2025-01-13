from django.contrib import admin
from django.urls import path, include

from profitpages.apps import ProfitpagesConfig
from profitpages.views import (
    PublicationListView,
    PublicationCreateView,
    PublicationDetailView,
)

app_name = ProfitpagesConfig.name


urlpatterns = [
    path("", PublicationListView.as_view(), name="main"),
    path("publication/create/", PublicationCreateView.as_view(), name="publication_create"),
    path("publication/detail/<int:pk>/", PublicationDetailView.as_view(), name="publication_detail"),
]
