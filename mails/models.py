# Create your models here.
from django.db import models
from django.urls import reverse


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    writer = models.CharField(max_length=20)

    is_sent = models.BooleanField(default=False)
    is_successfully_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("mails:email_save_view", kwargs={"pk": self.pk})
