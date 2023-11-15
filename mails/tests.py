from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from faker import Faker

from .models import Email
from .views import EmailSaveView

User = get_user_model()

fake = Faker()
dummy_subject = fake.sentence(nb_words=6)
dummy_message = fake.paragraph(nb_sentences=4)
dummy_writer = fake.first_name()

# class EmailSaveViewTest(TestCase):
#     def setUp(self):
#         self.email = EmailFactory()
#         self.user = User.objects.create_user(
#             username="testuser", password="testpass", email="test@test.com"
#         )

#     def test_email_save_view(self):
#         self.client.login(username="testuser", password="testpass")
#         print(self.email.__dict__)
#         response = self.client.post(
#             resolve_url("mails:email_save_view"), data=self.email.__dict__
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["subject"], self.email.subject)
#         self.assertEqual(response.data["message"], self.email.message)
#         self.assertEqual(response.data["writer"], self.email.writer)
#         self.assertEqual(response.data["is_sent"], self.email.is_sent)
#         self.assertEqual(
#             response.data["is_successfully_sent"], self.email.is_successfully_sent
#         )
#         self.assertEqual(response.data["is_read"], self.email.is_read)


class EmailSaveTest(TestCase):
    # 전체 테스트에 적용되는 데이터
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@test.com",
            nickname="testnick",
        )
        cls.valid_email = Email.objects.create(
            subject=dummy_subject, message=dummy_message, writer=dummy_writer
        )

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
            },
        )

        response_save = EmailSaveView.as_view()(request_send)

        result = Email.objects.get(id=email_id).is_successfully_sent
        self.assertTrue(result)
        self.assertIn(request_save.status_code, [200, 207])
