from django.db.models.signals import post_save
from django.dispatch import receiver

from bookmarks_app.models import Bookmark
from services.tasks import task_ran_parser_bookmark_by_id


@receiver(post_save, sender=Bookmark)
def post_save_bookmarks(sender: Bookmark, instance: Bookmark, created: bool, **kwargs):
    """Запуск задачи при первом сохранении закладки"""
    if created:
        task_ran_parser_bookmark_by_id.delay(instance.id)
