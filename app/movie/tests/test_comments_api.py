from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Comment

from movie.serializers import CommentSerializer


COMMENTS_URL = reverse('movies:comment-list')


class CommentsApiTests(TestCase):

    """ Test module for GET all comments API """
    def setUp(self):
        Comment.objects.create(
            movie_id=1,
            post_date='2019-01-01',
            comment_body="Very bad movie, wasted time"
        )
        Comment.objects.create(
            movie_id=1,
            post_date='2012-03-15',
            comment_body="Cute movie, like!"
        )

    def test_get_all_comments(self):
        """Test retrieving comments"""
        client = APIClient()
        response = client.get(COMMENTS_URL)
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_successful(self):
        """Test creating a new comment"""
        payload = {
            'movie_id': 15,
            'comment_body': "I didn't like that"
        }
        res = self.client.post(COMMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid(self):
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
        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
