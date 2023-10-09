from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from dj_rest_auth.views import UserDetailsView
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.serializers import (
    ReaderProfileSerializer,
    SendVerificationEmailSerializer,
    UserSerializer,
    WriterProfileSerializer,
)

from .models import User, VerificationEmail


class SignupView(dj_reg_views.RegisterView):
    pass


class SigninView(dj_auth_views.LoginView):
    pass


class SignoutView(dj_auth_views.LogoutView):
    pass


class SendVerificationEmailView(generics.CreateAPIView):
    queryset = VerificationEmail.objects.all()
    serializer_class = SendVerificationEmailSerializer

    def create(self, request, *args, **kwargs):
        """
        VerificationEmail 테이블에 튜플을 추가하고 인증 메일을 발송하는 메소드
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        email = self.get_queryset().filter(**serializer.validated_data).first()
        if email and not email.is_verified:
            email.send(request)

        return Response(
            {"detail": "인증 메일이 발송되었습니다."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ResendVerificationEmailView(generics.UpdateAPIView):
    pass


class VerifyEmailView(generics.RetrieveAPIView):
    pass


# TODO: define UserInfoView for retrieve, update, delete user info using dj_rest_auth
class UserInfoView(UserDetailsView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user

        if user.is_writer:
            return WriterProfileSerializer
        elif user.is_reader:
            return ReaderProfileSerializer
        else:
            return UserSerializer


class WriterListView(ListAPIView):
    query_set = User.objects.filter(is_writer=True)
    serializer_class = WriterProfileSerializer


class ReaderListView(ListAPIView):
    query_set = User.objects.filter(is_reader=True)
    serializer_class = ReaderProfileSerializer
