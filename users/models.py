from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", help_text="Введите ваше имя", **NULLABLE
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", help_text="Введите вашу фамилию"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите дополнительное описание", **NULLABLE
    )
    phone = models.CharField(
        unique=True,
        max_length=35,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", **NULLABLE
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.first_name
