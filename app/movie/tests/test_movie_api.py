from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Movie

from movie.serializers import MovieSerializer

import requests


MOVIES_URLS = reverse('movies:movie-list')


def sample_movie(movie_name):
    """Fetching movie and assigning to model"""
    requested_movie = movie_name.lower().strip().replace(' ', '+')
    api_key = '8a16ad04'
    response = requests.get(
        f'http://www.omdbapi.com/?t={requested_movie}&apikey={api_key}'
    )
    params = response.json()
    sample_movie = Movie.objects.create(
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
    return sample_movie


class MoviesApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_movie_successful(self):
        """Tests for retrieving movies successfully"""
        sample_movie('Pulp Fiction')
        sample_movie('unbroken')
        res = self.client.get(MOVIES_URLS)

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_movie_not_found(self):
        """Tests for movie not found in external api"""
        requested_movie = 'I like to dance'.lower().strip().replace(' ', '+')
        api_key = '8a16ad04'
        response = requests.get(
            f'http://www.omdbapi.com/?t={requested_movie}&apikey={api_key}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['Error'], 'Movie not found!')
