from django.urls import path
from .views import MovieListCreate, MovieRetrieveUpdateDelete, WatchMovie, CommentListCreate, RatingListCreate

urlpatterns = [
    path('movies/', MovieListCreate.as_view()),                # GET, POST
    path('movies/<int:pk>/', MovieRetrieveUpdateDelete.as_view()),  # GET, PUT, DELETE
    path('movies/<int:pk>/watch/', WatchMovie.as_view()),     # GET
    path('movies/<int:movie_id>/ratings/', RatingListCreate.as_view(), name='movie-ratings'),
    path('movies/<int:movie_id>/comments/', CommentListCreate.as_view(), name='movie-comments'),
]
