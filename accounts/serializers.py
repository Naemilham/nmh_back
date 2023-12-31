from allauth.socialaccount.models import EmailAddress
from dj_rest_auth.registration import serializers as dj_reg_serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from django.core import validators
from rest_framework import serializers as rest_serializers
from rest_framework.validators import UniqueValidator

from accounts.models import ReaderProfile, User, VerificationEmail, WriterProfile


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

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise rest_serializers.ValidationError(
                ("The two password fields didn't match.")
            )
        if (
            not VerificationEmail.objects.filter(email=data["email"]).exists()
            or not VerificationEmail.objects.get(email=data["email"]).is_verified
        ):
            raise rest_serializers.ValidationError(("Given email is not verified."))
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get("nickname")
        user.is_writer = self.validated_data.get("is_writer")
        user.is_reader = self.validated_data.get("is_reader")
        user.save()
        return user


class SendVerificationEmailSerializer(rest_serializers.ModelSerializer):
    def validate_email(self, data):
        validators.validate_email(data)
        return data

    class Meta:
        model = VerificationEmail
        fields = (
            "id",
            "email",
        )


class VerifyEmailSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = VerificationEmail
        fields = (
            "email",
            "verification_code",
            "is_verified",
        )
        read_only_fields = (
            "email",
            "is_verified",
        )

    def update(self, instance, validated_data):
        instance.is_verified = True
        instance.save()
        return instance


class UserSerializer(UserDetailsSerializer):
    def to_representation(self, instance):
        res = super().to_representation(instance)
        if instance.is_writer:
            res.update({"profile_id": instance.writerprofile.id})
        elif instance.is_reader:
            res.update({"profile_id": instance.readerprofile.id})
        return res

    class Meta:
        model = User
        fields = ("id", "username", "nickname", "email", "is_writer", "is_reader")
        read_only_fields = ("email",)


class WriterProfileSerializer(UserDetailsSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = WriterProfile
        fields = (
            "user",
            "self_introduction",
            "mailing_introduction",
            "example",
        )


class ReaderProfileSerializer(UserDetailsSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ReaderProfile
        fields = ("user",)


class ProfileIdSerializer(rest_serializers.ModelSerializer):
    def to_representation(self, instance):
        res = super().to_representation(instance)
        if instance.is_writer:
            res["writerprofile_id"] = instance.writerprofile.id
        elif instance.is_writer:
            res["readerprofile_id"] = instance.readerprofile.id
        return res

    class Meta:
        model = User
        fields = ()
