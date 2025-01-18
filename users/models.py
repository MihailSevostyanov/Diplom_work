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
        max_length=50,
        verbose_name="Фамилия",
        help_text="Введите вашу фамилию",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="О себе", help_text="Введите информацию о себе", **NULLABLE
    )
    phone = models.CharField(
        unique=True,
        max_length=35,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    created_at = models.DateField(
        verbose_name="Дата создания профиля", auto_now_add=True, **NULLABLE
    )
    is_subscribed = models.BooleanField(default=False, verbose_name="Подписка")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.first_name


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        related_name="payment",
        **NULLABLE,
    )
    price = models.PositiveIntegerField(verbose_name="сумма оплаты")
    session_id = models.CharField(max_length=300, verbose_name="id сессии")
    is_paid = models.BooleanField(
        default=False, verbose_name="Статус прохождения платежа"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания платежа"
    )
    paid_at = models.DateTimeField(verbose_name="Дата оплаты", **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

        def __str__(self):
            return f"{self.user} - {self.price}"
