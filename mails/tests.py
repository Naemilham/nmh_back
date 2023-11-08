from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from faker import Faker

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
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpass", email="test@test.com"
        )

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
