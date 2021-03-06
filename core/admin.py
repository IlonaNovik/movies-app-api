from django.contrib import admin
from core import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'post_date', 'comment_body')
    list_display_links = ('id',)
    list_filter = ['movie_id', 'post_date']
    search_fields = ('movie_id', 'post_date', 'comment_body')
    list_per_page = 25


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year')
    list_display_links = ('id', 'title')
    list_filter = ['id', 'title', 'genre']
    search_fields = ('id', 'title', 'genre')
    list_per_page = 25


class TopAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'total_comments', 'rank')
    list_display_links = ('id', )
    list_filter = ['movie_id', 'total_comments', 'rank']
    search_fields = ('movie_id', 'total_comments', 'rank')
    list_per_page = 25


admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Top, TopAdmin)
