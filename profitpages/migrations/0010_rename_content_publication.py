# Generated by Django 5.1.4 on 2025-01-13 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profitpages", "0009_content_updated_at"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Content",
            new_name="Publication",
        ),
    ]
