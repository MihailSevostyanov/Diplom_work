# Generated by Django 5.1.4 on 2025-01-17 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_payment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="paid_it",
            new_name="paid_at",
        ),
    ]
