import random
import string

from django.contrib.auth import models as auth_models
from django.contrib.auth import validators
from django.core.mail import send_mail
from django.db import models as db_models
from django.utils import timezone

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


class VerificationEmail(db_models.Model):
    email = db_models.EmailField(unique=True, null=True)
    verification_code = db_models.TextField(null=True)
    is_verified = db_models.BooleanField(default=False)
    sent_at = db_models.DateTimeField(null=True)

    def create_verification_code(self):
        """
        영어 대소문자 + 숫자로 이루어진 12자리 인증 코드 생성하는 메소드
        """
        LENGTH = 12
        string_pool = string.ascii_letters + string.digits
        code = ""

        for _ in range(LENGTH):
            code += random.choice(string_pool)

        return code

    @property
    def _verification_code(self):
        return self.create_verification_code()

    def send_verification_mail(self, request):
        """
        인증 메일 발송을 요청한 메일 주소로 메일을 발송하는 메소드
        """
        subject = "내밀함 회원가입 인증 메일"
        message = self._verification_code
        recipient = [request.data.get("email")]
        is_successfully_sent = send_mail(
            subject, message, from_email=None, recipient_list=recipient
        )

        if is_successfully_sent:
            self.verification_code = message[:]
            self.sent_at = timezone.now()
            self.save()
            return True

        return False

    def verify_email(self, verification_code, request):
        """
        사용자가 입력한 인증 번호가 서버에서 발급한 인증 번호와 일치하는지 확인하는 메소드
        """
        if verification_code == request.data.get("verification_code"):
            return True
        return False
