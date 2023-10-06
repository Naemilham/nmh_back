# Create your models here.
from django.db import models


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    writer = models.CharField(max_length=20)
    recipient_list = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True)
    is_successfully_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
