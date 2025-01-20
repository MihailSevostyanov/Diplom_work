from django.urls import path
from django.views.decorators.cache import cache_page

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
    publication_set_paid,
    my_webhook_view, set_user_is_publisher,
)
from users.views import payment_success, payment_cancel

app_name = ProfitpagesConfig.name


urlpatterns = [
    path("", PublicationListView.as_view(), name="main"),
    path("publication/create/", cache_page(10)(PublicationCreateView.as_view()), name="publication_create"),
    path("publication/detail/<int:pk>/", cache_page(10)(PublicationDetailView.as_view()), name="publication_detail"),
    path("publication/update/<int:pk>/", cache_page(10)(PublicationUpdateView.as_view()), name="publication_update"),
    path("publication/delete/<int:pk>/", cache_page(10)(PublicationDeleteView.as_view()), name="publication_delete"),
    path("author/<int:pk>/publications/", cache_page(10)(PublicationAuthorlistView.as_view()), name="publication_author"),

    path("subscription/", cache_page(120)(buy_subscription), name="subscription_create"),
    path("webhooks/stripe/", my_webhook_view, name="stripe_webhook"),
    path("payment_success/", payment_success, name="payment_success"),
    path("payment_cancel/", payment_cancel, name="payment_cancel"),
    path("publication_set_paid/<int:pk>/", publication_set_paid, name="publication_set_paid"),
    path("set_user_is_publisher/<int:pk>/", set_user_is_publisher, name="set_user_is_publisher"),

    path("publisher/", cache_page(10)(PublisherListView.as_view()), name="publisher_list"),  # TODO: add search functionality!
    path("publisher/create/",cache_page(10)(PublisherCreateView.as_view()), name="publisher_create"),
    path("publisher/detail/<int:pk>/", cache_page(10)(PublisherDetailView.as_view()), name="publisher_detail"),
    path("publisher/update/<int:pk>/", cache_page(10)(PublisherUpdateView.as_view()), name="publisher_update"),
    path("publisher/delete/<int:pk>/", cache_page(10)(PublisherDeleteView.as_view()), name="publisher_delete"),
]
