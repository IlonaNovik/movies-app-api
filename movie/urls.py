from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from movie import views

schema_view = get_swagger_view(title='Movies Api Documentation')

router = DefaultRouter()
router.register('comments', views.CommentViewSet, basename='comment')
router.register('movies', views.MovieViewSet, basename='movie')
router.register('top', views.TopViewSet, basename='top')

app_name = 'movies'

urlpatterns = [
    path('docs', schema_view, name="schema_view"),
    path('', include(router.urls)),
]
