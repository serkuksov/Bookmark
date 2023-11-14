from config.celery import app
from services.base_task import BaseTaskWithRetry
from services.parsers import BookmarkParsingManager


@app.task(base=BaseTaskWithRetry)
def task_ran_parser_bookmark_by_id(bookmark_id: int) -> None:
    """Задача запускающая процесс парсинга закладки по ее id в БД"""
    BookmarkParsingManager(bookmark_id=bookmark_id).parse_and_save()
