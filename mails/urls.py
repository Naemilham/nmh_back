from django.urls import path

from .views import EmailDetailView, EmailListView, EmailSendView

app_name = "mails"
urlpatterns = [
    path("", EmailListView.as_view()),
    path("<int:pk>/", EmailDetailView.as_view()),
    path("send/", EmailSendView.as_view()),
]
