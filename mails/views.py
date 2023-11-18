from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from nmh.settings import DEFAULT_FROM_EMAIL

from .models import Email
from .serializer import EmailSerializer


class EmailView(APIView):
    def get(self, request):
        # DB에서 주어진 id에 맞는 이메일 반환
        email_id = request.data.get("email_id")

        try:
            email = Email.objects.get(id=email_id)
            response = Response(
                data=EmailSerializer(email).data, status=status.HTTP_200_OK
            )
        except Email.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)

        return response

    def post(self, request):
        email_id = request.data.get("email_id")

        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # subject, message, writer는 DB에서 가져오고 recipient_list는 writer의 writerProfile에서 subscribing_readers를 가져옴

        subject = email.subject
        message = email.message
        email.categories

        recipient_list = request.data.get("recipient_list")

        # with subscription model
        # subscriber_list = Subscribtion.objects.filter(subscribed_user=writer)
        # recipient_list = subscriber_list.values_list("subscribing_user", flat=True)
        # subscriber_list 중 메일 수신을 원치 않는 경우 필터링(categories_id 활용)

        if subject is None or message is None or recipient_list is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 메일 송신에 성공한 수
        success_count = 0

        for recipient in recipient_list:
            print(recipient)
            letter = EmailMessage(  # Create a new email object for each recipient
                subject=subject,
                body=message,
                from_email=DEFAULT_FROM_EMAIL,
                to=[recipient],
            )

            try:
                result = letter.send(fail_silently=True)
                success_count += result  # Increment the count for each successful send
                email.is_sent = True
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

    # 이메일 DB 전체 삭제하는 API
    def delete(self, request):
        Email._truncate()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailSaveView(APIView):
    # 이메일 저장하는 API
    def post(self, request):
        subject = request.data.get("subject")
        message = request.data.get("message")
        writer = request.data.get("writer")

        # exception handling
        if subject is None or message is None or writer is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response

    # 이메일 수정하는 API
    def put(self, request):
        email_id = request.data.get("email_id")

        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subject = request.data.get("subject")
        message = request.data.get("message")

        if subject is None or message is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serialiizer = EmailSerializer(email, data=request.data, partial=True)

        if serialiizer.is_valid():
            serialiizer.save()
            response = Response(data=serialiizer.data, status=status.HTTP_200_OK)
        else:
            response = Response(
                data=serialiizer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response

    # 개별 이메일 삭제하는 API
    def delete(self, request):
        email_id = request.data.get("email_id")

        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        email.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
