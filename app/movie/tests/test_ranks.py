from django.test import TestCase

from core.models import Comment, Top


def set_rank_for_movie(comments):
    """Function for setting rank to movies"""

    if len(comments) == 0:
        return {'details': 'No comments found for selected date range'}

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


class SetRankingTest(TestCase):
    """Class for testing movie rank"""

    def test_set_ranking_for_movies_successful(self):
        start_date = "2020-05-17"
        end_date = "2020-05-17"

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

        comments = Comment.objects.filter(
            post_date__range=[start_date, end_date]
        )
        top_movies = set_rank_for_movie(comments)

        self.assertEqual(top_movies[0].movie_id, 26)
        self.assertEqual(top_movies[0].total_comments, 3)
        self.assertEqual(top_movies[0].rank, 1)

        self.assertEqual(top_movies[1].movie_id, 30)
        self.assertEqual(top_movies[1].total_comments, 1)
        self.assertEqual(top_movies[1].rank, 2)

    def test_no_comments_for_selected_date_range(self):
        start_date = "2020-04-17"
        end_date = "2020-04-17"

        comments = Comment.objects.filter(
            post_date__range=[start_date, end_date]
        )

        result = {'details': 'No comments found for selected date range'}
        top_movies = set_rank_for_movie(comments)

        self.assertEqual(top_movies, result)

    def test_set_ranking_for_one_movie_found(self):
        start_date = "2020-05-17"
        end_date = "2020-05-17"

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
            post_date__range=[start_date, end_date]
        )
        top_movies = set_rank_for_movie(comments)

        self.assertEqual(top_movies[0].movie_id, 26)
        self.assertEqual(top_movies[0].total_comments, 2)
        self.assertEqual(top_movies[0].rank, 1)

    def test_set_ranking_for_many_movies_found(self):
        start_date = "2020-05-17"
        end_date = "2020-05-17"

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
            post_date__range=[start_date, end_date]
        )
        top_movies = set_rank_for_movie(comments)

        self.assertEqual(top_movies[0].movie_id, 26)
        self.assertEqual(top_movies[0].total_comments, 2)
        self.assertEqual(top_movies[0].rank, 2)
        self.assertEqual(top_movies[1].movie_id, 25)
        self.assertEqual(top_movies[1].total_comments, 1)
        self.assertEqual(top_movies[1].rank, 3)
        self.assertEqual(top_movies[2].movie_id, 30)
        self.assertEqual(top_movies[2].total_comments, 3)
        self.assertEqual(top_movies[2].rank, 1)
