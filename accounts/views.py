from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.serializers import (
    ReaderProfileSerializer,
    SendVerificationEmailSerializer,
    UserSerializer,
    VerifyEmailSerializer,
    WriterProfileSerializer,
)

from .models import ReaderProfile, User, VerificationEmail, WriterProfile


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
        if email.send_verification_mail(request):
            return Response(
                {"detail": "인증 메일이 발송되었습니다."},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

        return Response(
            {"detail": "인증 메일 발송에 실패했습니다."},
            status=status.HTTP_502_BAD_GATEWAY,
            headers=headers,
        )


class ResendVerificationEmailView(generics.UpdateAPIView):
    queryset = VerificationEmail.objects.all()
    serializer_class = SendVerificationEmailSerializer

    def perform_update(self, serializer):
        super().perform_update(serializer)
        email = self.get_object()
        if not email.send_verification_mail(serializer):
            return Response(
                {"detail": "인증 메일 발송에 실패했습니다."},
                status=status.HTTP_502_BAD_GATEWAY,
            )


class VerifyEmailView(generics.UpdateAPIView):
    queryset = VerificationEmail.objects.all()
    serializer_class = VerifyEmailSerializer

    def update(self, request, *args, **kwargs):
        """
        사용자로부터 인증을 요청받은 이메일이 이미 인증되었는지 확인하고,
        만약 미인증 상태라면 입력받은 인증 코드가 서버에서 발송한 인증 코드와 일치하는지 확인하는 메소드
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance.is_verified:
            return Response({"detail": "이미 인증 완료된 이메일입니다."})
        if instance.verify_email(instance.verification_code, request):
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({"detail: 인증 번호가 일치하지 않습니다."})


# TODO: define UserInfoView for retrieve, update, delete user info using dj_rest_auth
class UserInfoView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user

        if user.is_writer:
            return WriterProfileSerializer
        elif user.is_reader:
            return ReaderProfileSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_writer:
            return WriterProfile.objects.all()
        elif user.is_reader:
            return ReaderProfile.objects.all()
        else:
            return User.objects.all()


class WriterListView(ListAPIView):
    query_set = User.objects.filter(is_writer=True)
    serializer_class = WriterProfileSerializer


class ReaderListView(ListAPIView):
    query_set = User.objects.filter(is_reader=True)
    serializer_class = ReaderProfileSerializer
