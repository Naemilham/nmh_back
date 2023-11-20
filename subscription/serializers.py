from rest_framework import serializers, validators

from subscription import models


class SubscribeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if models.Subscription.objects.filter(
            subscribed_user=attrs["subscribed_user"],
            subscribing_user=attrs["subscribing_user"],
            categories_id=attrs["categories_id"],
        ).exists():
            raise validators.ValidationError("Duplicated subscription")

        return super().validate(attrs)

    class Meta:
        model = models.Subscription
        fields = "__all__"
