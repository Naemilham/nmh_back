from django.db.models.signals import post_save

from accounts import models


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.is_writer:
            models.WriterProfile.objects.create(user=user)
        elif user.is_reader:
            models.ReaderProfile.objects.create(user=user)


post_save.connect(create_profile, sender=models.User)
