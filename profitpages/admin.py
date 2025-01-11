from django.contrib import admin

from profitpages.models import Publisher, Content


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("nickname", "description", "user")


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "publisher")
