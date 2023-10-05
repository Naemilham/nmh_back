from dj_rest_auth.registration import views as dj_reg_views
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response, status

from .models import ReaderProfile, WriterProfile
from .serializers import ReaderProfileSerializer, WriterProfileSerializer


class SignupView(dj_reg_views.RegisterView):
    pass


# TODO: define UserInfoView for retrieve, update, delete user info using dj_rest_auth
class UserInfoView(RetrieveUpdateDestroyAPIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = request.user
        # isWriter, isReader 체크 후 writer, reader profile 반환
        if user.is_writer:
            writer_profile = WriterProfile.objects.get(user=user)
            serializer = WriterProfileSerializer(writer_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            reader_profile = ReaderProfile.objects.get(user=user)
            serializer = ReaderProfileSerializer(reader_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class UserListView(dj_reg_views.UserListView):
    pass
