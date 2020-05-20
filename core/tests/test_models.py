from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_create_comment_str(self):
        """Test for the comment representation"""
        comment = models.Comment.objects.create(
            movie_id=1,
            post_date="2020-01-01",
            comment_body="Very nice movie"
        )

        self.assertEqual(str(comment), comment.comment_body)

    def test_create_movie_str(self):
        """Test creating movie representation"""
        movie = models.Movie.objects.create(
            title="Big Fish",
            year="2003",
            released="09 Jan 2004",
            runtime="125 min",
            genre="Adventure, Drama, Fantasy, Romance",
            director="Tim Burton",
            writer="Daniel Wallace (novel), John August (screenplay)",
            actors="Ewan McGregor, Albert Finney, Billy Crudup, Jessica Lange",
            plot=("A frustrated son tries to determine the fact from " +
                    "fiction in his dying father's life."),
            language="English, Cantonese",
            country="USA",
            awards="Nominated for 1 Oscar. Another 68 nominations.",
            poster=("https://m.media-amazon.com/images/M/MV5BMmU3NzIyO" +
                    "DctYjVhOC00NzBmLTlhNWItMzBlODEwZTlmMjUzXkEyXkFqc" +
                    "GdeQXVyNTIzOTk5ODM @._V1_SX300.jpg"
                    ),
            imdb_rating="8.0",
            box_office="$66,257,002",
            production="Sony Pictures",
            website="N/A",
        )

        self.assertEqual(str(movie), movie.title)
