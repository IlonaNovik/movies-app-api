from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from movie.serializers import TopSerializer

from core.models import Comment, Top


def set_rank_for_movie(comments):
    """Function for setting rank to movies"""

    movie_id_list = []

    for comment in comments:
        movie_id_list.append(
            comment.movie_id
        )

    counters = {i: movie_id_list.count(i) for i in movie_id_list}

    length = len(counters)
    result = []

    if length == 1:
        for key, value in counters.items():
            temp = Top.objects.create(
                movie_id=key, total_comments=value, rank=1
            )
            result.append(temp)

    elif length == 2:
        if len(counters.values()) != len(set(counters.values())):
            for key, value in counters.items():
                temp = Top.objects.create(
                    movie_id=key, total_comments=value, rank=1
                )
                result.append(temp)
        else:
            max_key = max(counters, key=counters.get)
            min_key = min(counters, key=counters.get)

            high = Top.objects.create(
                movie_id=max_key, total_comments=counters[max_key], rank=1
            )
            low = Top.objects.create(
                movie_id=min_key, total_comments=counters[min_key], rank=2
            )

            result.append(high)
            result.append(low)

    elif length > 2:
        all_values = counters.values()
        max_value = max(all_values)
        min_value = min(all_values)

        if max_value == min_value:
            for key, value in counters.items():
                temp = Top.objects.create(
                    movie_id=key, total_comments=value, rank=1
                )
                result.append(temp)
        else:
            for key, value in counters.items():

                if value == max_value:
                    temp = Top.objects.create(
                        movie_id=key, total_comments=value, rank=1
                    )
                    result.append(temp)

                elif value == min_value:
                    temp = Top.objects.create(
                        movie_id=key, total_comments=value, rank=3
                    )
                    result.append(temp)

                else:
                    temp = Top.objects.create(
                        movie_id=key, total_comments=value, rank=2
                    )
                    result.append(temp)

            counter = 0
            for item in result:
                if item.rank == 2:
                    counter += 1
            if counter == 0:
                for item in result:
                    if item.rank == 3:
                        item.rank = 2

    return result


TOPS_URL = reverse('movies:top-list')


class SetRankingTest(TestCase):
    """Class for testing movie rank"""

    def setUp(self):
        self.client = APIClient()

    def test_get_error_when_request_all_top(self):
        """Test getting error when retrieve top"""

        res = self.client.get(TOPS_URL)
        error = {''
                 'detail': "Missing required parameters" +
                           " start_date and end_date"
                 }
        self.assertEqual(res.data, error)
        self.assertEqual(
            res.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_set_ranking_for_movies_successful(self):
        """Test for setting ranking to movies dependent
        on amount of comments during specified time period"""

        Comment.objects.create(
            movie_id=26,
            comment_body="Great movie",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=26,
            comment_body="Perfect movie to fall asleep",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=26,
            comment_body="Like!",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=30,
            comment_body="Superman one love <3",
            post_date="2020-05-17"
        )

        payload = {
            'start_date': "2020-05-17",
            'end_date': "2020-05-17"
        }
        comments = Comment.objects.filter(
            post_date__range=[payload['start_date'], payload['end_date']]
        )
        top_movies = set_rank_for_movie(comments)
        res = self.client.get(TOPS_URL, payload)
        serializer = TopSerializer(top_movies, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_no_comments_for_selected_date_range(self):
        payload = {
            'start_date': "2020-05-17",
            'end_date': "2020-05-17"
        }
        error = {
                 'detail': "No comments found for selected date range"
                 }

        res = self.client.get(TOPS_URL, payload)
        self.assertEqual(res.data, error)
        self.assertEqual(
            res.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_set_ranking_for_one_movie_found(self):
        payload = {
            'start_date': "2020-05-17",
            'end_date': "2020-05-17"
        }

        Comment.objects.create(
            movie_id=26,
            comment_body="Great movie",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=26,
            comment_body="Perfect movie to fall asleep",
            post_date="2020-05-17"
        )

        comments = Comment.objects.filter(
            post_date__range=[payload['start_date'], payload['end_date']]
        )

        top_movies = set_rank_for_movie(comments)
        res = self.client.get(TOPS_URL, payload)
        serializer = TopSerializer(top_movies, many=True)
        print(serializer.data)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_set_ranking_for_many_movies_found(self):
        payload = {
            'start_date': "2020-05-17",
            'end_date': "2020-05-17"
        }

        Comment.objects.create(
            movie_id=26,
            comment_body="Great movie",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=26,
            comment_body="Perfect movie to fall asleep",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=25,
            comment_body="Great movie",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=30,
            comment_body="Perfect movie to fall asleep",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=30,
            comment_body="Great movie",
            post_date="2020-05-17"
        )
        Comment.objects.create(
            movie_id=30,
            comment_body="Perfect movie to fall asleep",
            post_date="2020-05-17"
        )

        comments = Comment.objects.filter(
            post_date__range=[payload['start_date'], payload['end_date']]
        )

        top_movies = set_rank_for_movie(comments)
        sorted_top_movies = sorted(top_movies, key=lambda x: x.rank)
        res = self.client.get(TOPS_URL, payload)
        serializer = TopSerializer(sorted_top_movies, many=True)
        print(top_movies)
        print(serializer)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
