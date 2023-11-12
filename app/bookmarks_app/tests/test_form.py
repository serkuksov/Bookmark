from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ..models import Bookmark
from ..forms import BookmarkForm


class BaseTestCase(TestCase):
    """Базовый класс для наполнения БД"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="123456",
        )
        self.bookmark = Bookmark.objects.create(
            user=self.user,
            bookmark_url="https://test1.com/",
            created_at=datetime.now() - timedelta(hours=1),
        )
        self.bookmark = Bookmark.objects.create(
            user=self.user,
            bookmark_url="https://test2.com/",
            title="title2",
            description="description2",
            favicon_url="https://test2.com/favicon.ico",
            created_at=datetime.now(),
        )


@override_settings(CELERY_BROKER_URL="memory://")
class BookmarkFormTest(BaseTestCase):
    """Тесты формы добавления закладки пользователем"""

    def test_valid_data(self):
        form_data = {"bookmark_url": "https://test3.com/"}
        form = BookmarkForm(data=form_data, instance=Bookmark(user=self.user))

        self.assertTrue(form.is_valid())

    def test_duplicate_bookmark(self):
        form_data = {"bookmark_url": "https://test2.com/"}
        form = BookmarkForm(data=form_data, instance=Bookmark(user=self.user))

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Закладка с текущим URL уже существует для данного пользователя",
            form.errors["bookmark_url"],
        )

    def test_save_method(self):
        form_data = {"bookmark_url": "https://test4.com"}
        form = BookmarkForm(data=form_data, instance=Bookmark(user=self.user))

        bookmark = form.save()
        bookmark_db = Bookmark.objects.get(id=bookmark.id)
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark, bookmark_db)
