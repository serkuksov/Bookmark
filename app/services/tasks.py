from config.celery import app
from .parsers import BookmarkParsingManager


@app.task(bind=True)
def task_ran_parser_bookmark_by_id(self, bookmark_id: int) -> None:
    """Задача запускающая процесс парсинга закладки по ее id в БД"""
    try:
        BookmarkParsingManager(bookmark_id=bookmark_id).parse_and_save()
    except Exception as exc:
        # повторная попытка выполнения задачи
        self.retry(exc=exc, countdown=60, max_retries=2)
