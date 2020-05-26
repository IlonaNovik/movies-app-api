from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Comment, Movie

from movie.serializers import CommentSerializer

import requests


COMMENTS_URL = reverse('movies:comment-list')


def sample_movie(title):
    format_title = title.lower().strip().replace(' ', '+')
    api_key = '8a16ad04'
    response = requests.get(
        f'http://www.omdbapi.com/?t={format_title}&apikey={api_key}'
    )
    params = response.json()
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
    return retrieved_movie


class CommentsApiTests(TestCase):

    """ Test module for comments API """
    def setUp(self):
        self.client = APIClient()

    def test_get_all_comments(self):
        """Test retrieving comments"""
        movie1 = sample_movie('Shrek')
        new_comment = Comment.objects.create(
            movie_id=movie1.id,
            comment_body="I didn't like that"
        )
        movie1.comments.add(new_comment)

        response = self.client.get(COMMENTS_URL)
        comments = Comment.objects.all().order_by('-post_date')
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_successful(self):
        """Test creating a new comment"""
        movie = sample_movie('Shrek')
        payload = {
            'movie_id': movie.id,
            'comment_body': "I didn't like that"
        }
        res = self.client.post(COMMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_comment_invalid(self):
        """Test creating a new comment with invalid payload"""
        payload1 = {
            'movie_id': '',
            'post_date': '2012-03-15',
            'comment_body': "I didn't like that"
        }
        payload2 = {
            'movie_id': '14',
            'post_date': '2012-03-15',
            'comment_body': ""
        }
        res1 = self.client.post(COMMENTS_URL, payload1)
        res2 = self.client.post(COMMENTS_URL, payload2)
        self.assertEqual(
            res1.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            res2.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_retrieve_comments_assigned_to_movie(self):
        """Test filtering comments by movie id"""
        movie1 = sample_movie('Shrek')
        new_comment1 = Comment.objects.create(
            movie_id=movie1.id,
            comment_body="I didn't like that"
        )
        movie2 = sample_movie('Green Mile')
        new_comment2 = Comment.objects.create(
            movie_id=movie2.id,
            comment_body="My kids like it a lot"
        )
        movie1.comments.add(new_comment1)
        movie2.comments.add(new_comment2)

        res = self.client.get(
            COMMENTS_URL, {'movie_id': new_comment2.movie_id}
        )

        serializer1 = CommentSerializer(new_comment1)
        serializer2 = CommentSerializer(new_comment2)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
