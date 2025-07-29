from django.urls import path
from .views import MovieListCreate, MovieRetrieveUpdateDelete, WatchMovie

urlpatterns = [
    path('movies/', MovieListCreate.as_view()),                # GET, POST
    path('movies/<int:pk>/', MovieRetrieveUpdateDelete.as_view()),  # GET, PUT, DELETE
    path('movies/<int:pk>/watch/', WatchMovie.as_view()),     # GET
]
