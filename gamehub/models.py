from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Platform(models.Model):
    name = models.CharField(max_length=100)


class Game(models.Model):
    igdb_id = models.IntegerField()
    name = models.CharField(max_length=100)
    cover = models.URLField()
    slug = models.SlugField()
    first_release_date = models.DateField()
    rating = models.FloatField()
    rating_count = models.IntegerField()
    aggregated_rating = models.FloatField()
    aggregated_rating_count = models.IntegerField()
    summary = models.TextField()
    genres = models.ManyToManyField(Genre)
    platforms = models.ManyToManyField(Platform)


class Screenshot(models.Model):
    url = models.URLField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
