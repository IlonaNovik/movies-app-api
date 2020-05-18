from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Top

from movie.serializers import TopSerializer


TOP_URL = reverse('movies:top-list')


class TopApiTests(TestCase):

    """ Test module for ranking movies API """
    def setUp(self):
        self.client = APIClient()

    def test_get_all_ranking(self):
        """Test retrieving rankings"""

        response = self.client.get(TOP_URL)
        tops = Top.objects.all().order_by('rank')
        serializer = TopSerializer(tops, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_top_movies(self):
        """Test for retrieving top movies by amount of comments
        during specified period of time"""
