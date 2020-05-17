from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from core.models import Comment, Movie
from movie import serializers

import requests


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage comments in the database"""
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        """Filtering comments by movie id"""
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id')
        if movie_id:
            return queryset.filter(movie_id=movie_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """Creating a comment and assigning to a movie"""
        if request.data['movie_id'] and request.data['comment_body']:
            movie_id_request = request.data['movie_id']
            comment_body = request.data['comment_body']
            movie = Movie.objects.filter(id=int(movie_id_request))[0]

            if movie:
                new_comment = Comment.objects.create(
                    movie_id=int(movie_id_request),
                    comment_body=comment_body
                )
                new_comment.save()
                movie.comments.add(new_comment)
                serializer = serializers.CommentSerializer(new_comment)
                return Response(serializer.data)
            else:
                return Response(
                    data={
                        'detail': 'Movie with requested id' +
                        ' not found in database'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data={
                    'detail': 'Error! Post request contains empty fields'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies in database"""
    serializer_class = serializers.MovieSerializer

    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

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
                    data={
                        'detail': 'The movie title does not' +
                                  ' exist or is incorrect'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
