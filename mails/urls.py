from django.urls import path

from .views import EmailDetailView, EmailListView, EmailReplyView, EmailSendView

app_name = "mails"
urlpatterns = [
    path("", EmailListView.as_view()),
    path("<int:pk>/", EmailDetailView.as_view()),
    path("send/", EmailSendView.as_view()),
    path("reply/", EmailReplyView.as_view()),
]
