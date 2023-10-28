from django.contrib.auth import get_user_model
from django.db import models


class Bookmark(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    bookmark_url = models.URLField(verbose_name="Ссылка")
    title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Заголовок"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    favicon_url = models.URLField(blank=True, null=True, verbose_name="Фавикон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"
        unique_together = ("user", "bookmark_url")
