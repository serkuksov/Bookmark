from django.apps import AppConfig
from django.db.models.signals import post_save


class LinksAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookmarks_app"
    verbose_name = "Bookmark"

    def ready(self):
        """Регистрация сигнала"""
        from .signals import post_save_bookmarks

        post_save.connect(post_save_bookmarks, sender="bookmarks_app.Bookmark")
