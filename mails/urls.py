from django.urls import path

from .views import EmailSaveView, EmailView

app_name = "mails"
urlpatterns = [
    path("", EmailView.as_view()),
    path("/content", EmailSaveView.as_view()),
]
