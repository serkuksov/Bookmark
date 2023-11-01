from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTest(TestCase):
    """Тест регистрации нового пользователя"""

    def test_register_user(self):
        form_data = {
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }

        response = self.client.post(reverse("register"), data=form_data)

        self.assertEqual(response.status_code, 302)

        users_count = get_user_model().objects.count()

        self.assertEqual(users_count, 1)
        self.assertRedirects(response, reverse("login"))

    def test_register_existing_user(self):
        get_user_model().objects.create_user(username="test", password="123456")

        form_data = {
            "username": "test",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }

        response = self.client.post(reverse("register"), data=form_data)

        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response,
            "form",
            "username",
            "Пользователь с таким именем уже существует.",
        )
