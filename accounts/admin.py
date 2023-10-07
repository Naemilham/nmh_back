from django.contrib import admin

from accounts import models

admin.site.register(models.User)
admin.site.register(models.WriterProfile)
admin.site.register(models.ReaderProfile)
