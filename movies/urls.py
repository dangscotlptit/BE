from django.urls import path
from .views import (
    MovieListCreate, MovieRetrieveUpdateDelete, WatchMovie,
    CommentListCreate, RatingListCreate,
    GenreListCreate, GenreRetrieveUpdateDelete, MoviesByGenre
)

urlpatterns = [
    path('movies/', MovieListCreate.as_view()),                # GET, POST
    path('movies/<int:pk>/', MovieRetrieveUpdateDelete.as_view()),  # GET, PUT, PATCH, DELETE
    path('movies/<int:pk>/watch/', WatchMovie.as_view()),     # GET
    path('movies/<int:movie_id>/ratings/', RatingListCreate.as_view(), name='movie-ratings'),
    path('movies/<int:movie_id>/comments/', CommentListCreate.as_view(), name='movie-comments'),

    # Genre endpoints
    path('genres/', GenreListCreate.as_view(), name='genre-list-create'),  # GET, POST
    path('genres/<int:pk>/', GenreRetrieveUpdateDelete.as_view(), name='genre-detail'),  # GET, PUT, PATCH, DELETE
    path('genres/<int:genre_id>/movies/', MoviesByGenre.as_view(), name='movies-by-genre'),

]