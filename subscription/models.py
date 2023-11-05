from django.db import models as db_models

from accounts import models as accounts_models


class Subscription(db_models.Model):
    subscribed_user = db_models.ForeignKey(accounts_models.WriterProfile)
    subscribing_user = db_models.ForeignKey(accounts_models.ReaderProfile)
    created_at = db_models.DateTimeField(auto_now_add=True)
