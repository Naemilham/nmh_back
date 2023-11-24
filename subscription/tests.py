from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from .views import SubscribeView, UnsubscribeView

User = get_user_model()


class SubscriptionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create_user(
            username="testreader",
            password="testpass",
            email="reader@reader.com",
            nickname="testnick",
            is_reader=True,
            is_writer=False,
        )
        cls.writer = User.objects.create_user(
            username="testwriter",
            password="testpass",
            email="writer@writer.com",
            nickname="writer",
            is_reader=False,
            is_writer=True,
        )

    def setUp(self):
        self.factory = RequestFactory()

    def test_subscribe(self):
        request_valid = self.factory.post(
            "api/subscription/subscribe/",
            data={
                "subscribing_user": self.reader.id,
                "subscribed_user": self.writer.id,
                "categories_id": None,
            },
        )

        request_invalid = self.factory.post(
            "api/subscription/subscribe/",
            data={"subscribing_user": self.reader.id},
        )

        request_not_reader = self.factory.post(
            "api/subscription/subscribe/",
            data={
                "subscribing_user": self.writer.id,
                "subscribed_user": self.reader.id,
                "categories_id": None,
            },
        )

        response_valid = SubscribeView.as_view()(request_valid)
        response_invalid = SubscribeView.as_view()(request_invalid)
        response_not_reader = SubscribeView.as_view()(request_not_reader)

        self.assertEqual(response_valid.status_code, 201)
        self.assertEqual(response_invalid.status_code, 400)
        self.assertEqual(response_not_reader.status_code, 400)

    def test_unsubscribe(self):
        request_before_subscribe = self.factory.post(
            "api/subscription/unsubscribe/",
            data={
                "subscribing_user": self.reader.id,
                "subscribed_user": self.writer.id,
                "categories_id": None,
            },
        )

        request_subscribe = self.factory.post(
            "api/subscription/subscribe/",
            data={
                "subscribing_user": self.reader.id,
                "subscribed_user": self.writer.id,
            },
        )

        request_invalid = self.factory.post(
            "api/subscription/unsubscribe/",
            data={
                "subscribing_user": self.reader.id + 1,
                "subscribed_user": self.writer.id,
            },
        )

        request_valid = self.factory.post(
            "api/subscription/unsubscribe/",
            data={
                "subscribing_user": self.reader.id,
                "subscribed_user": self.writer.id,
            },
        )

        response_before_subscribe = UnsubscribeView.as_view()(request_before_subscribe)
        response_subscribe = SubscribeView.as_view()(request_subscribe)
        response_invalid = UnsubscribeView.as_view()(request_invalid)
        response_valid = UnsubscribeView.as_view()(request_valid)

        self.assertEqual(response_before_subscribe.status_code, 400)
        self.assertEqual(response_subscribe.status_code, 201)
        self.assertEqual(response_invalid.status_code, 400)
        self.assertEqual(response_valid.status_code, 200)
