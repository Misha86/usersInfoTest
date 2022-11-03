"""Module for all project tests."""
import tempfile

from django.test import TestCase
from django.urls import reverse
from django.test import Client

from .models import CustomUser
from django.contrib.auth.hashers import check_password


class CustomUserModelTest(TestCase):
    """Tests for CustomUser model behavior."""

    def setUp(self) -> None:
        self.superuser = CustomUser.objects.create_superuser(username="username1", password="password1")
        self.user = CustomUser.objects.create_user(username="username2", password="password2")

    def test_count_created_users(self):
        self.assertEqual(CustomUser.objects.all().count(), 2)

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


class ViewsTest(TestCase):
    """Tests for all views."""

    def setUp(self) -> None:
        self.client = Client()
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        CustomUser.objects.create_user(username="username", password="password", avatar=image)
        CustomUser.objects.create_superuser(username="superuser", password="superuser", avatar=image)

    def test_post_login_valid_data(self):
        response = self.client.post(reverse('login'), {'username': 'username', 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_post_login_invalid_data(self):
        response = self.client.post(reverse('login'), {'username': 'invalid', 'password': 'invalid'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.context['error'], "Inputted data is incorrect!")

    def test_get_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_get_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_users_list_for_user(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            users_list = response.context['users_list']

    def test_users_list_for_superuser(self):
        self.client.post(reverse('login'), {'username': 'superuser', 'password': 'superuser'})
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users_list']), 1)

    def test_get_upload_files_for_superuser(self):
        self.client.post(reverse('login'), {'username': 'superuser', 'password': 'superuser'})
        response = self.client.get(reverse('upload_files'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])
