from django.db import models

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
        help_text="Введите имя пользователя",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"

    def __str__(self):
        return self.nickname


class Content(models.Model):
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
        **NULLABLE
    )
    paid = models.BooleanField(default=False, help_text="Укажите тип контента:(Платный/Бесплатный)", verbose_name="Платный")
    preview = models.ImageField(upload_to="publication/preview", verbose_name="Превью", help_text="Загрузите превью публикации", **NULLABLE)

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title
