# Generated by Django 4.2.5 on 2023-11-13 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_verificationemail"),
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WriterCategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_writer",
                        to="categories.category",
                    ),
                ),
                (
                    "writer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="writer_category",
                        to="accounts.writerprofile",
                    ),
                ),
            ],
        ),
    ]
