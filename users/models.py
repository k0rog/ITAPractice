from django.contrib.auth.models import AbstractUser
from django.db import models
from gamehub.models import Game


class CustomUser(AbstractUser):
    age = models.IntegerField(null=True)
    musts = models.ManyToManyField(Game)
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
