from django.contrib.auth import models as auth_models
from django.contrib.auth import validators
from django.db import models as db_models

from accounts import managers


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    username_validator = validators.UnicodeUsernameValidator()

    username = db_models.CharField(
        max_length=150, unique=True, validators=[username_validator]
    )
    nickname = db_models.CharField(max_length=150, unique=True)
    email = db_models.EmailField(unique=True)
    is_reader = db_models.BooleanField(default=False)
    is_writer = db_models.BooleanField(default=False)
    is_staff = db_models.BooleanField(default=False)
    is_active = db_models.BooleanField(default=True)
    created_at = db_models.DateTimeField(auto_now_add=True)
    is_superuser = db_models.BooleanField(default=False)

    objects = managers.UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nickname", "email"]

    def __str__(self):
        return self.username


class WriterProfile(db_models.Model):
    user = db_models.OneToOneField(User, on_delete=db_models.CASCADE)
    self_introduction = db_models.TextField(blank=True)
    mailing_introduction = db_models.TextField(blank=True)
    example = db_models.TextField(blank=True)


class ReaderProfile(db_models.Model):
    user = db_models.OneToOneField(User, on_delete=db_models.CASCADE)
