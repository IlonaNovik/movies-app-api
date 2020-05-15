from rest_framework import serializers

from core.models import Comment

from _datetime import date


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment object"""
    post_date = serializers.ReadOnlyField(default=date.today)

    class Meta:
        model = Comment
        fields = ('movie_id', 'comment_body', 'post_date')
