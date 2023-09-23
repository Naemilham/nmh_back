from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class EmailView(APIView):
    def post(self, request):
        send_mail(
            "내밀함 이메일 발송 테스트",
            "제군들 들리는가.",
            "isuh88@naver.com",
            [
                "akk808@naver.com",
                "tjrwodnjs99@gmail.com",
                "uzinfamily@snu.ac.kr",
                "isuh88@gmail.com",
            ],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)
