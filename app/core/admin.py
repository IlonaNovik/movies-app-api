from django.contrib import admin
from core import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'post_date', 'comment_body')
    list_display_links = ('id',)
    list_filter = ['movie_id', 'post_date']
    search_fields = ('movie_id', 'post_date', 'comment_body')
    list_per_page = 25


admin.site.register(models.Comment, CommentAdmin)
