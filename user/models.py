"""Module for all project models."""
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUserManager(BaseUserManager):
    """This class provides tools for creating and managing CustomUser model."""

    def create_user(self, password, **additional_fields):
        """Creates CustomUser. Saves user instance with given fields values."""
        user = self.model(**additional_fields,)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password, **additional_fields):
        """Creates superuser. Saves instance with given fields values."""
        user = self.create_user(password, **additional_fields)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """This class represents a custom User model."""

    avatar = models.ImageField(blank=True, null=True, upload_to="images/")

    objects = MyUserManager()

    class Meta:
        """This metaclass stores verbose names ordering data."""

        ordering = ["id"]
        verbose_name = "User"
        verbose_name_plural = "Users"
