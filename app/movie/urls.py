from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movie import views

router = DefaultRouter()
router.register('comments', views.CommentViewSet)

app_name = 'movies'

urlpatterns = [
    path('', include(router.urls))
]
