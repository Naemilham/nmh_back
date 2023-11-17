from django.db import models as db_models

from accounts import models as accounts_models
from categories import models as categories_models


class Subscription(db_models.Model):
    subscribed_user = db_models.ForeignKey(
        accounts_models.WriterProfile, on_delete=db_models.CASCADE
    )
    subscribing_user = db_models.ForeignKey(
        accounts_models.ReaderProfile, on_delete=db_models.CASCADE
    )
    created_at = db_models.DateTimeField(auto_now_add=True)
    categories_id = db_models.ForeignKey(
        categories_models.Category,
        on_delete=db_models.SET_NULL,
        null=True,
        related_name="subscribed",
    )
