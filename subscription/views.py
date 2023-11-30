from rest_framework import generics, status
from rest_framework.response import Response

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
