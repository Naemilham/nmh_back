from rest_framework import serializers, validators

from accounts import models as acc_models
from subscription import models as sub_models


class SubscribeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not acc_models.ReaderProfile.objects.filter(
            id=attrs["subscribing_user"].id
        ).exists():
            raise validators.ValidationError("없는 독자입니다.")
        if not acc_models.WriterProfile.objects.filter(
            id=attrs["subscribed_user"].id
        ).exists():
            raise validators.ValidationError("없는 작가입니다.")
        if sub_models.Subscription.objects.filter(
            subscribed_user=attrs["subscribed_user"],
            subscribing_user=attrs["subscribing_user"],
            categories_id=attrs["categories_id"],
        ).exists():
            raise validators.ValidationError("이미 구독한 작가입니다.")

        return super().validate(attrs)

    class Meta:
        model = sub_models.Subscription
        fields = "__all__"


class UnsubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = sub_models.Subscription
        fields = ("subscribed_user", "subscribing_user")
