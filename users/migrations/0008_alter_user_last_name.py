# Generated by Django 5.1.4 on 2025-01-15 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_user_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True,
                help_text="Введите вашу фамилию",
                max_length=50,
                null=True,
                verbose_name="Фамилия",
            ),
        ),
    ]
