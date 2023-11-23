# Generated by Django 4.2.5 on 2023-11-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0001_initial"),
        ("accounts", "0002_verificationemail"),
    ]

    operations = [
        migrations.AddField(
            model_name="writerprofile",
            name="subscribing_readers",
            field=models.ManyToManyField(
                blank=True,
                related_name="subscribing_writers",
                through="subscription.Subscription",
                to="accounts.readerprofile",
            ),
        ),
    ]