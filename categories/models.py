from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    related_mails = models.ManyToManyField("Email", through="EmailCategory")


class EmailCategory(models.Model):
    id = models.AutoField(primary_key=True)
    email_id = models.ForeignKey(
        "Email", on_delete=models.CASCADE, related_name="email_category"
    )
    category_id = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="category_email"
    )
