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

        subject = email.subject
        writer = email.writer
        message = email.message

        # 메일 카테고리명 리스트
        categories = email.categories.values_list("category_name", flat=True)

        # writer_id = WriterProfile.objects.get(user).id

        recipient_list = request.data.get("recipient_list")

        # 구독 중인 reader들의 이메일 주소를 리스트로 저장
        # subscibing_readers = WriterProfile.objects.get(id=writer_id).subscribing_readers
        # recipient_list = subscibing_readers.values_list("email", flat=True)

        # subscriber_list 중 메일 수신을 원치 않는 경우 필터링(categories_id 활용)

        if subject is None or message is None or recipient_list is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 메일 송신에 성공한 수
        success_count = 0

        # HTML 양식에 맞춰 메일 내용을 렌더링
        email_html = render_to_string(
            "email_template.html",
            {
                "subject": subject,
                "writer": writer,
                "message": message,
                "categories": categories,
            },
        )

        for recipient in recipient_list:
            # 메일 발송 객체 생성
            letter = EmailMessage(
                subject=subject,
                from_email=DEFAULT_FROM_EMAIL,
                to=[recipient],
                reply_to=["isuh88@gmail.com"],
            )

            # 발송 메일 형식을 지정된 HTML 양식으로 포맷
            letter.content_subtype = "html"
            letter.body = email_html

            try:
                # 메일 발송
                email.is_sent = True

                # 메일 발송에 성공하면 success_count를 1 증가
                result = letter.send(fail_silently=True)
                success_count += result

                # 메일 발송에 성공하면 is_successfully_sent를 True로 변경
                email.is_successfully_sent = True if result else False

                email.save()
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
