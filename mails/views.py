from django.core.mail import EmailMessage, send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class EmailView(APIView):
    def get(self, request):
        title = request.data.get("title")
        content = request.data.get("content")
        to = request.data.get("to")
        send_mail(title, content, "naemilham@naver.com", to, fail_silently=False)
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        subject = request.data.get("subject")
        message = request.data.get("message")
        to = request.data.get("to")
        send_mail = EmailMessage(subject, message, to)
        try:
            send_mail.send()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
