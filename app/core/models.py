from django.db import models
from datetime import date


class Comment(models.Model):
    """Comment to be added to movie"""
    movie_id = models.IntegerField()
    post_date = models.DateField(default=date.today)
    comment_body = models.TextField()

    def __str__(self):
        return self.comment_body


class Movie(models.Model):
    """Movie model"""
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=20, blank=True)
    released = models.CharField(max_length=255, blank=True)
    runtime = models.CharField(max_length=20, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    director = models.CharField(max_length=255, blank=True)
    writer = models.CharField(max_length=255, blank=True)
    actors = models.CharField(max_length=255, blank=True)
    plot = models.TextField(blank=True)
    language = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    awards = models.TextField(blank=True)
    poster = models.URLField(max_length=200, blank=True)
    imdb_rating = models.DecimalField(
        max_digits=5, decimal_places=1, default=1.0
    )
    box_office = models.CharField(max_length=255, blank=True)
    production = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    comments = models.ManyToManyField('Comment')
    rank = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Top(models.Model):
    """Model for ranking movies"""
    movie_id = models.IntegerField()
    total_comments = models.IntegerField()
    rank = models.IntegerField()
