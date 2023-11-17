from rest_framework import generics

from subscription import models, permissions, serializers


class SubscribeView(generics.CreateAPIView):
    permission_classes = [permissions.IsReader]
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscribeSerializer


class UnsubscribeView(generics.DestroyAPIView):
    permission_classes = [permissions.IsReader]
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscribeSerializer
