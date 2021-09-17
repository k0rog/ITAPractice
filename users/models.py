from django.contrib.auth.models import AbstractUser
from django.db import models
from gamehub.models import Game


class CustomUser(AbstractUser):
    age = models.IntegerField()
    musts = models.ManyToManyField(Game)
