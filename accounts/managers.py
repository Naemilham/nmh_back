from django.apps import apps
from django.contrib.auth import base_user, hashers


class UserManager(base_user.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, nickname, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        if not nickname:
            raise ValueError("The given nickname must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(
            username=username, nickname=nickname, email=email, **extra_fields
        )
        user.password = hashers.make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, username, nickname=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, nickname, email, password, **extra_fields)

    def create_superuser(
        self, username, nickname=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, nickname, email, password, **extra_fields)
