from django.contrib import admin
from django.urls import path, include

from profitpages.apps import ProfitpagesConfig
from profitpages.views import (
    PublicationListView,
    PublicationCreateView,
    PublicationDetailView,
    PublicationUpdateView,
    PublicationDeleteView,

    PublicationAuthorlistView,
    PublisherCreateView,
    PublisherDetailView,
    PublisherUpdateView,
    PublisherDeleteView,
    PublisherListView,

    buy_subscription,
    publication_set_paid, my_webhook_view,
)
from users.views import payment_success, payment_cancel

app_name = ProfitpagesConfig.name


urlpatterns = [
    path("", PublicationListView.as_view(), name="main"),
    path("publication/create/", PublicationCreateView.as_view(), name="publication_create"),
    path("publication/detail/<int:pk>/", PublicationDetailView.as_view(), name="publication_detail"),
    path("publication/update/<int:pk>/", PublicationUpdateView.as_view(), name="publication_update"),
    path("publication/delete/<int:pk>/", PublicationDeleteView.as_view(), name="publication_delete"),

    path("author/<int:pk>/publications/", PublicationAuthorlistView.as_view(), name="publication_author"),
    path("subscription/", buy_subscription, name="subscription_create"),
    path('webhooks/stripe/', my_webhook_view, name='stripe_webhook'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_cancel/', payment_cancel, name='payment_cancel'),
    path("publication_set_paid/<int:pk>/", publication_set_paid, name='publication_set_paid'),

    path("publisher/", PublisherListView.as_view(), name="publisher_list"),  # TODO: add search functionality!
    path("publisher/create/", PublisherCreateView.as_view(), name="publisher_create"),
    path("publisher/detail/<int:pk>/", PublisherDetailView.as_view(), name="publisher_detail"),
    path("publisher/update/<int:pk>/", PublisherUpdateView.as_view(), name="publisher_update"),
    path("publisher/delete/<int:pk>/", PublisherDeleteView.as_view(), name="publisher_delete"),
]
