from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from bookmarks_app.models import Bookmark, Statys


@override_settings(CELERY_BROKER_URL="memory://")
class SignalTest(TestCase):
    """Тест сигнала"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="123456",
        )

    @patch("services.tasks.task_ran_parser_bookmark_by_id.delay")
    def test_save_method(self, mock_task: Mock):
        bookmark = Bookmark.objects.create(
            user=self.user,
            bookmark_url="https://test3.com/",
        )

        # Проверьте, что функция task_ran_parser_bookmark_by_id.delay была вызвана с правильным аргументом (ID закладки)
        mock_task.assert_called_with(bookmark.id)

        bookmark.statys = Statys.EXECUTED
        bookmark.save()

        # Проверяем, что метод delay был вызван только один раз
        mock_task.assert_called_once()
