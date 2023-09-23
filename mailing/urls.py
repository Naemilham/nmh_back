from django.contrib import admin
from django.urls import path
from .views import EmailView

app_name = 'mailing'
urlpatterns = [
    path('', EmailView.as_view()),
]