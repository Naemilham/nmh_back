from django.db import models as db_models


class Category(db_models.Model):
    category_id = db_models.AutoField(primary_key=True)
    category_name = db_models.CharField(max_length=100, unique=True)
    related_mails = db_models.ManyToManyField("mails.Email", through="EmailCategory")

    def __str__(self):
        return self.category_name


class EmailCategory(db_models.Model):
    id = db_models.AutoField(primary_key=True)
    email_id = db_models.ForeignKey(
        "mails.Email", on_delete=db_models.CASCADE, related_name="email_category"
    )
    category_id = db_models.ForeignKey(
        "Category", on_delete=db_models.CASCADE, related_name="category_email"
    )


class WriterCategory(db_models.Model):
    # category와 writer를 연결하는 테이블
    id = db_models.AutoField(primary_key=True)
    writer_id = db_models.ForeignKey(
        "accounts.WriterProfile",
        on_delete=db_models.CASCADE,
        related_name="writer_category",
    )
    category_id = db_models.ForeignKey(
        "Category", on_delete=db_models.CASCADE, related_name="category_writer"
    )
