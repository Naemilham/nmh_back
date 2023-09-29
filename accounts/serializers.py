from allauth.socialaccount.models import EmailAddress
from dj_rest_auth.registration import serializers as dj_reg_serializers
from rest_framework import serializers as rest_serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User


class SignupSerializer(dj_reg_serializers.RegisterSerializer):
    email = rest_serializers.EmailField(
        validators=[UniqueValidator(queryset=EmailAddress.objects.all())]
    )
    nickname = rest_serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    is_writer = rest_serializers.BooleanField(default=False)
    is_reader = rest_serializers.BooleanField(default=False)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "nickname": self.validated_data.get("nickname", ""),
            "is_writer": self.validated_data.get("is_writer", ""),
            "is_reader": self.validated_data.get("is_reader", ""),
        }

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get("nickname")
        user.is_writer = self.validated_data.get("is_writer")
        user.is_reader = self.validated_data.get("is_reader")
        user.save()
        return user
