from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from accounts.managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    objects = CustomUserManager()

    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_reader = models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nickname", "email"]

    def __str__(self):
        return self.username
