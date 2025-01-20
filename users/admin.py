from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "description",
        "created_at",
        "is_publisher",
        "is_subscribed",
        "is_superuser",
        "is_staff",
        "phone",
        "pk",
    )
    list_filter = ("email", "is_superuser")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "price",
        "session_id",
        "is_paid",
        "created_at",
        "paid_at",
        "pk",
    )
    list_filter = ("created_at",)
