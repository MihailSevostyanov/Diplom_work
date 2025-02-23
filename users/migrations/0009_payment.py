# Generated by Django 5.1.4 on 2025-01-15 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_user_last_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.PositiveIntegerField(verbose_name="сумма оплаты")),
                (
                    "session_id",
                    models.CharField(max_length=300, verbose_name="id сессии"),
                ),
                (
                    "is_paid",
                    models.BooleanField(
                        default=False, verbose_name="Статус прохождения платежа"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания платежа"
                    ),
                ),
                (
                    "paid_it",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата оплаты"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
