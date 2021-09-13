from django.db import models


class Game(models.Model):
    igdb_id = models.IntegerField()
