from celery import Task
from requests.exceptions import HTTPError

from bookmarks_app.models import Bookmark, Statys
from config.celery import app
from .parsers import BookmarkParsingManager


class BaseTaskWithRetry(Task):
    autoretry_for = (HTTPError,)
    retry_kwargs = {
        "max_retries": 5,
        "countdown": 60,
    }
    retry_backoff = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        bookmark = Bookmark.objects.get(id=args[0])
        bookmark.statys = Statys.ERROR
        bookmark.save()


@app.task(base=BaseTaskWithRetry)
def task_ran_parser_bookmark_by_id(bookmark_id: int) -> None:
    """Задача запускающая процесс парсинга закладки по ее id в БД"""
    BookmarkParsingManager(bookmark_id=bookmark_id).parse_and_save()
