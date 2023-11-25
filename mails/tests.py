from django.test import RequestFactory, TestCase
from faker import Faker

from accounts.models import User, WriterProfile

from .models import Email
from .views import EmailSaveView, EmailView

fake = Faker()
dummy_subject = fake.sentence(nb_words=6)
dummy_message = fake.paragraph(nb_sentences=4)
dummy_writer = fake.first_name()
dummy_recipient_list = [fake.email() for _ in range(5)]


class EmailSaveTest(TestCase):
    # 전체 테스트에 적용되는 데이터
    @classmethod
    def setUpTestData(cls):
        cls.valid_email = Email.objects.create(
            subject=dummy_subject, message=dummy_message, writer=dummy_writer
        )
        cls.writer = User.objects.create_user(
            username=dummy_writer,
            password="testpass",
            email="writer@writer.com",
            nickname="writer",
            is_reader=False,
            is_writer=True,
        )
        cls.writerProfile = WriterProfile.objects.create(user=cls.writer)

    # 트랜잭션에 의해 테스트 별로 롤백되는 데이터
    def setUp(self):
        self.factory = RequestFactory()

    # 각 테스트는 트랜잭션 적용
    def test_email_save(self):
        request = self.factory.post(
            "mails/save/",
            data={
                "subject": dummy_subject,
                "message": dummy_message,
                "writer": dummy_writer,
            },
        )

        response = EmailSaveView.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_email_save_with_invalid_data(self):
        request_1 = self.factory.post(
            "mails/save/",
            data={
                "subject": dummy_subject,
                "message": dummy_message,
            },
        )

        request_2 = self.factory.post(
            "mails/save/",
            data={
                "subject": dummy_subject,
                "writer": dummy_writer,
            },
        )

        request_3 = self.factory.post(
            "mails/save/",
            data={
                "message": dummy_message,
                "writer": dummy_writer,
            },
        )

        response_1 = EmailSaveView.as_view()(request_1)
        response_2 = EmailSaveView.as_view()(request_2)
        response_3 = EmailSaveView.as_view()(request_3)
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)

    def test_email_send(self):
        request_save = self.factory.post(
            "mails/save/",
            data={
                "subject": dummy_subject,
                "message": dummy_message,
                "writer": dummy_writer,
            },
        )
        response_save = EmailSaveView.as_view()(request_save)
        self.assertEqual(response_save.status_code, 201)

        email_id = response_save.data["id"]
        request_send = self.factory.post(
            "mails/send/",
            data={
                "email_id": email_id,
                "recipient_list": dummy_recipient_list,
            },
            content_type="application/json",
        )

        response_send = EmailView.as_view()(request_send)

        result = Email.objects.get(id=email_id).is_sent
        # TODO: 제대로 전송되는지 다시 확인!
        self.assertTrue(result)
        self.assertIn(response_send.status_code, [200, 207])
