from celery import Task


class BaseTaskWithRetry(Task):
    """Базовая задача с повторной попыткой"""

    retry_kwargs = {
        "max_retries": 5,
        "countdown": 60,
    }
    retry_backoff = True
