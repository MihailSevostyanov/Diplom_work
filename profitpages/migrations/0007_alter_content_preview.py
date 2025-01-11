# Generated by Django 5.1.4 on 2025-01-10 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profitpages", "0006_content_preview"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="preview",
            field=models.ImageField(
                blank=True,
                help_text="Загрузите превью публикации",
                null=True,
                upload_to="publication/preview",
                verbose_name="Превью",
            ),
        ),
    ]
