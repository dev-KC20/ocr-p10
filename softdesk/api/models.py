from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):

    email = models.EmailField(verbose_name='email address', unique=True,)  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "{}".format(self.email)


class Contributors(Users):
    pass
