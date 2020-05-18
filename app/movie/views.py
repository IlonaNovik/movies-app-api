from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from django.core.exceptions import ValidationError

from core.models import Comment, Movie, Top
from movie import serializers

from datetime import datetime
import requests
from .set_ranking import set_rank_for_movie


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage comments in the database"""
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        """Filtering comments by movie id"""
        try:
            queryset = Comment.objects.all()
            movie_id = self.request.query_params.get('movie_id')
            id_exists = Movie.objects.filter(id=movie_id)
            comments_exist = Comment.objects.filter(movie_id=movie_id)
            if movie_id:
                if id_exists and comments_exist:
                    return queryset.filter(movie_id=movie_id)
                elif id_exists and not comments_exist:
                    return Response(
                        data={
                            'detail': "No comments added for requested movie"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    raise APIException(
                        "Movie with requested id not found in database"
                    )
            return queryset
        except ValueError:
            raise APIException("Please enter correct movie id")

    def create(self, request, *args, **kwargs):
        """Creating a comment and assigning to a movie"""
        if request.data['movie_id'] and request.data['comment_body']:

            movie_id_request = request.data['movie_id']
            comment_body = request.data['comment_body']
            id_exists = Movie.objects.filter(id=int(movie_id_request))

            if id_exists:
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
                raise APIException(
                    "Movie with requested id not found in database"
                )
        else:
            raise APIException(
                "Error! Post request contains empty fields"
            )


class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies in database"""
    serializer_class = serializers.MovieSerializer

    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        queryset = Movie.objects.all()
        id = self.request.query_params.get('id')
        title = self.request.query_params.get('title')
        year = self.request.query_params.get('year')
        genre = self.request.query_params.get('genre')

        if id:
            id_exists = Movie.objects.filter(id=int(id))
            if id_exists:
                return queryset.filter(id=int(id))
            else:
                raise APIException(
                    "Movie with requested id does not exist in database"
                )
        if title:
            title_exists = Movie.objects.filter(title__icontains=title.lower())
            if title_exists:
                return queryset.filter(title__icontains=title.lower())
            else:
                raise APIException(
                    "Movie with requested title does not exist in database"
                )
        if year:
            year_exists = Movie.objects.filter(year=year)
            if year_exists:
                return queryset.filter(year=year)
            else:
                raise APIException(
                    "Movie with requested production " +
                    "year does not exist in database"
                )
        if genre:
            genre_exists = Movie.objects.filter(genre__icontains=genre)
            if genre_exists:
                return queryset.filter(genre__icontains=genre)
            else:
                raise APIException(
                    "Movie with requested genre does not exist in database"
                )
        return queryset

    def create(self, request, *args, **kwargs):
        movie_data = request.data['title'].lower().strip()
        titles_exist_in_db = Movie.objects.values_list('title', flat=True)

        if any(movie_data == title.lower() for title in titles_exist_in_db):
            raise APIException(
                "Requested movie title already exists in database"
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
                raise APIException(
                    "The movie title does not exist or is incorrect"
                )


class TopViewSet(viewsets.ModelViewSet):
    """Manage comments in the database"""

    """
    param1 -- A first parameter
    param2 -- A second parameter
    """
    serializer_class = serializers.TopSerializer

    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)
    queryset = Top.objects.all()

    def get_queryset(self):
        Top.objects.all().delete()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                comments = Comment.objects.filter(
                    post_date__range=[start_date, end_date]
                )
                """Date parameters and comments validation"""
                if end_date:
                    start_date_parsed = datetime.strptime(
                        start_date, '%Y-%m-%d'
                    )
                    end_date_parsed = datetime.strptime(
                        end_date, '%Y-%m-%d'
                    )
                    if start_date_parsed > datetime.now():
                        raise APIException(
                            "Start date cannot be in the future"
                        )
                    elif start_date_parsed > end_date_parsed:
                        raise APIException(
                            "Start date cannot be after the end date"
                        )
                if len(comments) == 0 and start_date and end_date:
                    raise APIException(
                        "No comments found for selected date range"
                    )
                else:
                    set_rank_for_movie(comments)
                    queryset = Top.objects.all().order_by('rank')

                    return queryset
            except ValidationError:
                raise APIException(
                    "Error! Requested parameters " +
                    "must be date format (yyyy-mm-dd)"
                )
        else:
            raise APIException(
                "Missing required parameters start_date and end_date"
            )
