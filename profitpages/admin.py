from django.contrib import admin

from profitpages.models import Publisher, Publication, Subscription


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("nickname", "description", "user", "pk")


@admin.register(Publication)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "publisher", "updated_at", "pk")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "update_at", "end_at", "pk")
