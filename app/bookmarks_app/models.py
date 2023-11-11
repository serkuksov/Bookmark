from django.contrib.auth import get_user_model
from django.db import models


class Statys(models.TextChoices):
    """Статусы"""

    PLANNED = "Planned", "Заплонировано"
    EXECUTED = "Executed", "Выполняется"
    DONE = "Done", "Выполнено"
    ERROR = "Error", "Ошибка"


class Bookmark(models.Model):
    """Модель закладки"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    bookmark_url = models.URLField(verbose_name="Ссылка")
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Заголовок",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    favicon_url = models.URLField(blank=True, null=True, verbose_name="Фавикон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    statys = models.CharField(
        choices=Statys.choices,
        default=Statys.PLANNED,
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"
        unique_together = ("user", "bookmark_url")
        ordering = ["-created_at"]
