from rest_framework import serializers

from core.models import Comment, Movie

from _datetime import date


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment object"""
    post_date = serializers.ReadOnlyField(default=date.today)

    class Meta:
        model = Comment
        fields = ('movie_id', 'comment_body', 'post_date')


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movies object"""
    # comments = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Comment.objects.all()
    # )
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'year',
            'released',
            'runtime',
            'genre',
            'director',
            'writer',
            'actors',
            'plot',
            'language',
            'country',
            'awards',
            'poster',
            'imdb_rating',
            'box_office',
            'production',
            'website',
            'rank',
            'comments',
        )
        read_only_fields = (
            'id',
            'year',
            'released',
            'runtime',
            'genre',
            'director',
            'writer',
            'actors',
            'plot',
            'language',
            'country',
            'awards',
            'poster',
            'imdb_rating',
            'box_office',
            'production',
            'website',
            'rank',
            'comments',
        )
