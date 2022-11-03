"""Module for all project tests."""
from django.test import TestCase
from .models import CustomUser
from django.contrib.auth.hashers import check_password


class CustomUserModelTest(TestCase):
    """Tests for CustomUser model behavior."""

    def setUp(self) -> None:
        self.superuser = CustomUser.objects.create_superuser(username="username1", password="password1")
        self.user = CustomUser.objects.create_user(username="username2", password="password2")

    def test_count_created_users(self):
        users = CustomUser.objects.all()
        self.assertEqual(users.count(), 2)

    def test_usernames_created_users(self):
        self.assertEqual(self.superuser.username, 'username1')
        self.assertEqual(self.user.username, 'username2')

    def test_password_created_users(self):
        self.assertTrue(check_password('password1', self.superuser.password))
        self.assertTrue(check_password('password2', self.user.password))

    def test_create_superuser(self):
        self.assertEqual(self.superuser.is_superuser, True)
        self.assertEqual(self.superuser.is_staff, True)
        self.assertNotEqual(self.user.is_superuser, True)

    def test_create_user_not_data(self):
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user()

