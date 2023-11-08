from rest_framework import serializers

from subscription import models


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = "__all__"
