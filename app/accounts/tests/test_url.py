from django.contrib.auth.views import LoginView, LogoutView
from django.test import TestCase
from django.urls import reverse, resolve

from accounts import views


class UrlsTestCase(TestCase):
    """Тесты URL"""

    def test_urls(self):
        self.assertEqual(resolve(reverse("login")).func.view_class, LoginView)
        self.assertEqual(resolve(reverse("logout")).func.view_class, LogoutView)
        self.assertEqual(
            resolve(reverse("register")).func.view_class, views.RegisterUser
        )

    def test_path_urls(self):
        self.assertEqual(reverse("login"), "/accounts/login/")
        self.assertEqual(reverse("logout"), "/accounts/logout/")
        self.assertEqual(reverse("register"), "/accounts/register/")
