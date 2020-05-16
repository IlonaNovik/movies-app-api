from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from core.models import Comment, Movie
from movie import serializers

import requests


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies in database"""
    serializer_class = serializers.MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        movie_data = request.data['title'].lower().strip()
        titles_exist_in_db = Movie.objects.values_list('title', flat=True)

        if any(movie_data == title.lower() for title in titles_exist_in_db):
            return Response(
                data={'detail': 'This movie title already exists in database'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            format_title = movie_data.lower().strip().replace(' ', '+')
            api_key = '8a16ad04'
            response = requests.get(
                f'http://www.omdbapi.com/?t={format_title}&apikey={api_key}'
            )
            params = response.json()

            try:
                retrieved_movie = Movie.objects.create(
                    title=params['Title'],
                    year=params['Year'],
                    released=params['Released'],
                    runtime=params['Runtime'],
                    genre=params['Genre'],
                    director=params['Director'],
                    writer=params['Writer'],
                    actors=params['Actors'],
                    plot=params['Plot'],
                    language=params['Language'],
                    country=params['Country'],
                    awards=params['Awards'],
                    poster=params['Poster'],
                    imdb_rating=params['imdbRating'],
                    box_office=params['BoxOffice'],
                    production=params['Production'],
                    website=params['Website'],
                )
                retrieved_movie.save()
                serializer = serializers.MovieSerializer(retrieved_movie)
                return Response(serializer.data)
            except KeyError:
                return Response(
                    data={'detail': 'The movie title does not exist or is incorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )
