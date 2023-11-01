from django.test import TestCase
from django.urls import reverse, resolve

from .. import views


class UrlsTestCase(TestCase):
    """Тесты URL"""

    def test_urls(self):
        self.assertEqual(
            resolve(reverse("bookmark_list")).func.view_class, views.BookmarkListView
        )
        self.assertEqual(
            resolve(reverse("add_bookmark")).func.view_class, views.BookmarkCreateView
        )

    def test_path_urls(self):
        self.assertEqual(reverse("bookmark_list"), "/")
        self.assertEqual(reverse("add_bookmark"), "/add_bookmark/")
