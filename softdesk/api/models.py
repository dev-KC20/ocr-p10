from django.db import models
from django.conf import settings

class Contributors():
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
