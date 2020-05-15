from django.db import models
from datetime import date


class Comment(models.Model):
    """Comment to be added to movie"""
    movie_id = models.IntegerField()
    post_date = models.DateField(default=date.today)
    comment_body = models.TextField()

    def __str__(self):
        return self.comment_body
