import html
import imaplib
import logging
import re

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from nmh.settings import DEFAULT_FROM_EMAIL

from .models import Email
from .serializer import EmailSerializer

logger = logging.getLogger("mails")


class EmailListView(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"List operation requested by user: {request.user}")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Create operation requested by user: {request.user}")
        return super().create(request, *args, **kwargs)


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieve operation requested by user: {request.user}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Update operation requested by user: {request.user}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Partial update operation requested by user: {request.user}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Destroy operation requested by user: {request.user}")
        return super().destroy(request, *args, **kwargs)


class EmailSendView(APIView):
    def post(self, request):
        email_id = request.data.get("email_id")

        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subject = email.subject
        message = email.message

        # 메일 작성자 WriterProfile 객체
        writer = email.writer

        # 메일 카테고리명 리스트
        categories = email.categories.values_list("category_name", flat=True)

        # is_reply_to_me = email.writer.is_reply_to_me

        recipient_list = request.data.get("recipient_list")

        # 구독 중인 reader들의 이메일 주소를 리스트로 저장
        # subscribing_readers = email.writer.subscribing_readers
        # recipient_list = subscibing_readers.values_list("email", flat=True)

        if subject is None or message is None or recipient_list is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 메일 송신에 성공한 수
        success_count = 0

        # HTML 양식에 맞춰 메일 내용을 렌더링
        email_html = render_to_string(
            "email_template.html",
            {
                "subject": subject,
                "writer": writer.user.username,
                "message": message,
                "categories": categories,
            },
        )

        # 고정된 메일 헤더 있을 시 추후 포함
        formatted_subject = f"[내밀함/{writer.id}] {subject}"

        for recipient in recipient_list:
            # 메일 발송 객체 생성
            letter = EmailMessage(
                subject=formatted_subject,
                from_email=DEFAULT_FROM_EMAIL,
                to=[recipient],
                reply_to=[DEFAULT_FROM_EMAIL],
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
                logger.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 메일 발송에 성공한 수에 따라 응답 메시지를 다르게 전송
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


class EmailReplyView(APIView):
    pattern = re.compile(r'charset="UTF-8".*?<div dir=3D"ltr">(.*?)</div>', re.DOTALL)

    def post(self, request):
        # 메일 서버 연결 후 로그인
        try:
            logger.debug("Connecting to mail server...")

            mail = imaplib.IMAP4_SSL(
                getattr(settings, "EMAIL_HOST_IMAP"),
                getattr(settings, "EMAIL_PORT_IMAP"),
                timeout=10,
            )
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            logger.debug("Connecting to mail account...")

            mail.login(
                getattr(settings, "EMAIL_HOST_USER"),
                getattr(settings, "EMAIL_HOST_PASSWORD"),
            )
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.debug("Successfully connected to mail server.")

        # 메일 UTF8 인코딩 설정 및 메일함 선택
        # mail.enable("UTF8=ACCEPT")                        # naver 메일은 지원하지 않음
        mail.select("_reply")

        logger.debug("Successfully selected '_reply' mail box.")

        # writer_encoded = request.data.get("writer").encode("utf-8")
        request.data.get("writer")
        # logger.debug(f"writer_encoded: {writer}")

        result, data = mail.search(None, "UNSEEN")
        if result == "OK":
            email_ids = data[0].split()

        # 읽지 않은 메일이 없을 경우
        else:
            logger.info("Failed to fetch email ids from '_reply' mail box.")
            return Response(status=status.HTTP_204_NO_CONTENT)

        logger.info("Successfully fetched email ids from '_reply' mail box.")

        email_content_list = []

        for email_id in email_ids:
            result, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            email_content_list.append([email_id, raw_email])

            match = self.pattern.search(raw_email.decode("utf-8"))
            if match:
                encoded_text = match.group(1)
                decoded_text = html.unescape(encoded_text)
                unicode_text = decoded_text = html.unescape(
                    encoded_text.replace("=", "%").encode("utf-8").decode("utf-8")
                )
                # 메일 객체 생성
                logger.debug(f"Encoded text: {encoded_text}")
                logger.debug(f"Decoded_text: {decoded_text}")
                logger.debug(f"Unicode text: {unicode_text}")

        # 메일함 삭제 및 연결 해제
        mail.close()

        # 메일 서버 로그아웃
        mail.logout()

        response = Response(
            status=status.HTTP_200_OK,
            data={"message": "success", "mail content": email_content_list},
        )

        return response
