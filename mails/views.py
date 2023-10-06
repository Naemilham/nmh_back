from django.core.mail import EmailMessage, send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from nmh.settings import DEFAULT_FROM_EMAIL

from .models import Email
from .serializer import EmailSerializer


class EmailSendView(APIView):
    def get(self, request):  # db에 저장된 이메일을 보내는 것으로 바꿔야 함, 임시로 GET으로 구현
        subject = request.data.get("subject")
        message = request.data.get("message")
        recipient_list = request.data.get("recipient_list")

        if subject is None or message is None or recipient_list is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=DEFAULT_FROM_EMAIL,
            bcc=recipient_list,
        )

        success_count = 0  # Count the number of successful sends

        for recipient in recipient_list:
            email = EmailMessage(  # Create a new email object for each recipient
                subject=subject,
                body=message,
                from_email=DEFAULT_FROM_EMAIL,
                to=[recipient],
            )

            try:
                email.send()
                success_count += 1  # Increment the count for each successful send
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    "message": "failed for some recipients",
                    "success_count": success_count,
                },
            )

        return response

    def post(self, request):
        email_id = request.data.get("email_id")
        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        sucessful_post = send_mail(
            email.subject,
            email.message,
            from_email=None,
            recipient_list=email.recipient_list,
        )

        if sucessful_post == len(email.recipient_list):
            email.is_sent = True
            email.is_successfully_sent = True
            response = Response(
                status=status.HTTP_200_OK,
                data={"message": "success for all recipients"},
            )
        elif sucessful_post == 0:
            email.is_sent = False
            email.is_successfully_sent = False
            response = Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"message": "failed for all recipients"},
            )
        else:
            email.is_sent = True
            email.is_successfully_sent = False
            response = Response(
                status=status.HTTP_207_MULTI_STATUS,
                data={"message": "fail for some recipients"},
            )
        return response


class EmailSaveView(APIView):
    def post(self, request):
        subject = request.data.get("subject")
        message = request.data.get("message")
        writer = request.data.get("writer")
        serializer = EmailSerializer(subject=subject, message=message, writer=writer)

        if serializer.is_valid():
            serializer.save()
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response
