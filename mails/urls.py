from django.urls import path

from .views import EmailView

app_name = "mails"
urlpatterns = [
    path("", EmailView.as_view()),
]
