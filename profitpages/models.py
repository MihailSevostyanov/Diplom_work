from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Publisher(models.Model):
    nickname = models.CharField(
        max_length=150,
        verbose_name="Псевдоним",
        help_text="Введите псевдоним автора",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание автора", **NULLABLE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя, который является владельцем издательства",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"

    def __str__(self):
        return self.nickname


class Publication(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Название публикации",
        help_text="Введите название публикации",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание публикации",
        help_text="Укажите описание публикации",
        **NULLABLE
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        help_text="Укажите автора публикации",
        related_name='publication',
        **NULLABLE
    )
    paid = models.BooleanField(default=False, help_text="Укажите тип контента:(Платный/Бесплатный)", verbose_name="Платный")
    preview = models.ImageField(upload_to="publication/preview", verbose_name="Превью", help_text="Загрузите превью публикации", **NULLABLE)
    content = CKEditor5Field(verbose_name='содержание публикации', config_name='extends', **NULLABLE)
    updated_at = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True, **NULLABLE)

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription')
    is_active = models.BooleanField(default=False, verbose_name="Активна ли подписка")
    update_at = models.DateTimeField(auto_now_add=True, verbose_name="Время обновления подписки", **NULLABLE)
    end_at = models.DateTimeField(verbose_name="Подписка активна до", **NULLABLE)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

