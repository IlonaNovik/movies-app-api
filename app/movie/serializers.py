from rest_framework import serializers

from core.models import Comment, Movie, Top

from _datetime import date


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment object"""
    post_date = serializers.ReadOnlyField(default=date.today)

    class Meta:
        model = Comment
        fields = ('movie_id', 'comment_body', 'post_date')


class CommentForMovieSerializer(serializers.ModelSerializer):
    """Serializer for display comments in movie object"""

    class Meta:
        model = Comment
        fields = ('comment_body', 'post_date')


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movies object"""
    # comments = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Comment.objects.all(),
    # )
    comments = CommentForMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'year', 'released', 'runtime',
            'genre', 'director', 'writer', 'actors', 'plot',
            'language', 'country', 'awards', 'poster', 'imdb_rating',
            'box_office', 'production', 'website', 'comments',
        )
        read_only_fields = (
            'id', 'year', 'released', 'runtime', 'genre',
            'director', 'writer', 'actors', 'plot', 'language',
            'country', 'awards', 'poster', 'imdb_rating',
            'box_office', 'production', 'website', 'comments',
        )


class TopSerializer(serializers.ModelSerializer):
    """Serializer for top ranking object"""

    class Meta:
        model = Top
        fields = (
            'movie_id', 'total_comments', 'rank'
        )
        read_only_fields = ('movie_id', 'total_comments', 'rank')
