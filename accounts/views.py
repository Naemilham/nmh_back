from dj_rest_auth.registration import views as dj_reg_views
from dj_rest_auth.views import UserDetailsView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import (
    ReaderProfileSerializer,
    UserSerializer,
    WriterProfileSerializer,
)

from .models import User


class SignupView(dj_reg_views.RegisterView):
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
