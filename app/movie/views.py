from rest_framework import viewsets, mixins

from core.models import Comment
from movie import serializers


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        """Create a new comment"""
        serializer.save()
