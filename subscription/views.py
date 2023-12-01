from rest_framework import generics
from rest_framework import permissions as rest_permissions
from rest_framework import status
from rest_framework.response import Response

from accounts import serializers as accounts_serializers
from subscription import models, permissions, serializers


class SubscribeView(generics.CreateAPIView):
    permission_classes = [permissions.IsReader, permissions.IsSelf]
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscribeSerializer


class UnsubscribeView(generics.CreateAPIView):
    permission_classes = [permissions.IsReader, permissions.IsSelf]
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.UnsubscribeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscribed_user = serializer.validated_data["subscribed_user"]
        subscribing_user = serializer.validated_data["subscribing_user"]
        headers = self.get_success_headers(serializer.data)

        instance = models.Subscription.objects.filter(
            subscribed_user=subscribed_user, subscribing_user=subscribing_user
        )
        if instance.exists():
            instance.delete()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, headers=headers)
        return Response(status=status.HTTP_200_OK, headers=headers)


class SubscribingWritersListView(generics.ListAPIView):
    permission_classes = [rest_permissions.IsAuthenticated]
    queryset = models.Subscription.objects.all()
    serializer_class = accounts_serializers.WriterProfileSerializer

    def get_queryset(self):
        user = self.request.user.readerprofile
        print(user)
        return user.subscribing_writers.all()


class SubscribingReadersListView(generics.ListAPIView):
    permission_classes = [rest_permissions.IsAuthenticated]
    queryset = models.Subscription.objects.all()
    serializer_class = accounts_serializers.ReaderProfileSerializer

    def get_queryset(self):
        user = self.request.user.writerprofile
        print(user)
        return user.subscribing_readers.all()
