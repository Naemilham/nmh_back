from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from nmh.settings import DEFAULT_FROM_EMAIL

from .models import Email
from .serializer import EmailSerializer


class EmailListView(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class EmailSendView(APIView):
    def post(self, request):
        email_id = request.data.get("email_id")

        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # subject, message, writer는 DB에서 가져오고 recipient_list는 writer의 writerProfile에서 subscribing_readers를 가져옴

        subject = email.subject
        writer = email.writer
        message = email.message
        email.categories

        # user = User.objects.get(username=writer)
        # writer_id = WriterProfile.objects.get(user).id

        recipient_list = request.data.get("recipient_list")

        # with subscription model
        # subscibing_readers = WriterProfile.objects.get(id=writer_id).subscribing_readers
        # recipient_list = subscibing_readers.values_list("email", flat=True)

        # subscriber_list 중 메일 수신을 원치 않는 경우 필터링(categories_id 활용)

        if subject is None or message is None or recipient_list is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 메일 송신에 성공한 수
        success_count = 0
        email_html = render_to_string(
            "email_template.html",
            {"subject": subject, "writer": writer, "message": message},
        )

        for recipient in recipient_list:
            letter = EmailMessage(  # Create a new email object for each recipient
                subject=subject,
                from_email=DEFAULT_FROM_EMAIL,
                to=[recipient],
            )

            # 발송 메일 형식을 지정된 HTML 양식으로 포맷
            letter.content_subtype = "html"
            letter.body = email_html

            try:
                email.is_sent = True
                result = letter.send(fail_silently=True)
                success_count += result  # Increment the count for each successful send
                email.is_successfully_sent = True if result else False
                email.save()  # 업데이트 내용 저장
            except Exception as e:
                print(e)  # Need to log this error

        if success_count == len(recipient_list):
            response = Response(
                status=status.HTTP_200_OK,
                data={
                    "message": "success for all recipients",
                    "success_count": success_count,
                },
            )
        elif success_count == 0:
            response = Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    "message": "failed for all recipients",
                    "success_count": success_count,
                },
            )
        else:
            response = Response(
                status=status.HTTP_207_MULTI_STATUS,
                data={
                    "message": "failed for some recipients",
                    "success_count": success_count,
                },
            )

        return response
