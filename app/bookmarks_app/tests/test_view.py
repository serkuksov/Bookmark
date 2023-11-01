from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Bookmark


class BaseTestCase(TestCase):
    """Базовый класс для наполнения БД"""

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user",
            password="123456",
        )
        self.bookmark1 = Bookmark.objects.create(
            user=self.user1,
            bookmark_url="https://test1.com/",
            created_at=datetime.now() - timedelta(hours=1),
        )
        self.bookmark2 = Bookmark.objects.create(
            user=self.user1,
            bookmark_url="https://test2.com/",
            title="title2",
            description="description2",
            favicon_url="https://test2.com/favicon.ico",
            created_at=datetime.now(),
        )

        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="123456",
        )
        self.bookmark3 = Bookmark.objects.create(
            user=self.user2,
            bookmark_url="https://test3.com/",
            created_at=datetime.now() - timedelta(hours=1),
        )


class BookmarkListViewTest(BaseTestCase):
    """Тест отображения списка закладок"""

    def test_view_with_authenticated_user(self):
        self.client.login(username=self.user1.username, password="123456")

        response = self.client.get(reverse("bookmark_list"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "https://test1.com")
        self.assertContains(response, "https://test1.com")
        self.assertNotContains(response, "https://test3.com")

    def test_view_with_unauthenticated_user(self):
        response = self.client.get(reverse("bookmark_list"))

        self.assertEqual(response.status_code, 302)

    def test_view_with_another_user(self):
        self.client.login(username=self.user2.username, password="123456")

        response = self.client.get(reverse("bookmark_list"))

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "https://test1.com")
        self.assertNotContains(response, "https://test1.com")
        self.assertContains(response, "https://test3.com")


@override_settings(CELERY_BROKER_URL="memory://")
class BookmarkCreateViewTest(BaseTestCase):
    """Тест отображения добавления закладок"""

    def test_create_bookmark(self):
        self.client.login(username=self.user1.username, password="123456")

        data = {
            "bookmark_url": "https://test4.com",
        }

        response = self.client.post(reverse("add_bookmark"), data)

        self.assertEqual(response.status_code, 302)

        bookmark = Bookmark.objects.get(bookmark_url="https://test4.com")
        self.assertEqual(bookmark.user, self.user1)

    def test_create_bookmark_with_invalid_data(self):
        self.client.login(username=self.user1.username, password="123456")

        data = {
            "bookmark_url": "invalid_url",
        }

        response = self.client.post(reverse("add_bookmark"), data)

        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response,
            "form",
            "bookmark_url",
            "Введите правильный URL.",
        )

    def test_create_bookmark_without_authentication(self):
        data = {
            "bookmark_url": "https://test4.com",
        }
        response = self.client.post(reverse("add_bookmark"), data)

        self.assertEqual(response.status_code, 302)

        with self.assertRaises(ObjectDoesNotExist):
            Bookmark.objects.get(bookmark_url="https://nonexistent.com")
