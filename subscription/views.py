from rest_framework import generics

from subscription import models, serializers


class SubscribeView(generics.CreateAPIView):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscribeSerializer
