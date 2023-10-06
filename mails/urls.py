from django.urls import path

from .views import EmailSaveView, EmailSendView

app_name = "mails"
urlpatterns = [
    path("send/", EmailSendView.as_view()),
    path("save/", EmailSaveView.as_view()),
]
