from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, override_settings

from bookmarks_app.models import Bookmark, Statys


@override_settings(CELERY_BROKER_URL="memory://")
class BookmarkModelTest(TestCase):
    """Тест модели закладок"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="123456",
        )
        self.bookmark1 = Bookmark.objects.create(
            user=self.user,
            bookmark_url="https://test1.com/",
            title="Test title",
            description="Test description",
            favicon_url="https://test1.com/favicon.ico",
            statys=Statys.PLANNED,
        )
        self.bookmark2 = Bookmark.objects.create(
            user=self.user,
            bookmark_url="https://test2.com/",
            title="Test title",
            description="Test description",
            favicon_url="https://test2.com/favicon.ico",
            statys=Statys.DONE,
        )

    def test_create_bookmark(self):
        bookmark = Bookmark.objects.create(
            user=self.user,
            bookmark_url="https://test3.com/",
        )

        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.bookmark_url, "https://test3.com/")
        self.assertIsNone(bookmark.title)
        self.assertIsNone(bookmark.description)
        self.assertIsNone(bookmark.favicon_url)
        self.assertIsInstance(bookmark.created_at, datetime)
        self.assertIsNotNone(bookmark.created_at)
        self.assertEqual(bookmark.get_statys_display(), "Заплонировано")

    def test_sorted_bookmark(self):
        bookmarks_db = Bookmark.objects.filter(user=self.user).all()

        self.assertEqual(len(bookmarks_db), 2)
        self.assertEqual(bookmarks_db[0], self.bookmark2)

    def test_constrained_unique_user_and_bookmark_url(self):
        with self.assertRaises(IntegrityError) as ex:
            Bookmark.objects.create(
                user=self.user,
                bookmark_url="https://test1.com/",
            )
        self.assertIn(
            "constraint",
            str(ex.exception),
        )

    def test_validate_statys(self):
        bookmark = Bookmark(
            user=self.user,
            bookmark_url="https://test3.com/",
            statys="test",
        )

        with self.assertRaises(ValidationError):
            bookmark.full_clean()
