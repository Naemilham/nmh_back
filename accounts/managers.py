from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, nickname, email, **extra_fields):
        if not email:
            raise ValueError("The Email must be set!")
        email = self.normalize_email(email)
        user = self.model(
            username=username, nickname=nickname, email=email, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, nickname, email, **extra_fields):
        user = self.create_user(
            username=username, nickname=nickname, email=email, password=password
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
