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
