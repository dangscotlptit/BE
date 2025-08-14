from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Genre, Movie, Comment, Rating

BASE_URL = "/api"  # API prefix


class AuthMixin:
    def authenticate_as(self, username, password):
        """Đăng nhập bằng JWT và set Authorization header."""
        res = self.client.post(f"{BASE_URL}/token/", {
            "username": username,
            "password": password
        })
        self.assertEqual(res.status_code, 200, f"Không lấy được token cho {username}")
        token = res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class AdminAPITest(APITestCase, AuthMixin):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.authenticate_as("admin", "adminpass")

        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            video_url="http://example.com/video.mp4",
            poster_url="http://example.com/poster.jpg",
            release_year=2024
        )
        self.movie.genres.add(self.genre)

    def test_create_genre_success(self):
        res = self.client.post(f"{BASE_URL}/genres/", {"name": "Comedy"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_genre_duplicate(self):
        res = self.client.post(f"{BASE_URL}/genres/", {"name": "Action"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_genre_success(self):
        res = self.client.put(f"{BASE_URL}/genres/{self.genre.id}/", {"name": "Adventure"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_genre_duplicate(self):
        Genre.objects.create(name="Drama")
        res = self.client.put(f"{BASE_URL}/genres/{self.genre.id}/", {"name": "Drama"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_genre_with_movies_fail(self):
        res = self.client.delete(f"{BASE_URL}/genres/{self.genre.id}/")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PublicAPITest(APITestCase, AuthMixin):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="userpass")
        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            video_url="http://example.com/video.mp4",
            poster_url="http://example.com/poster.jpg",
            release_year=2024
        )
        self.movie.genres.add(self.genre)

    def test_list_movies(self):
        res = self.client.get(f"{BASE_URL}/movies/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_watch_movie_increases_views(self):
        views_before = self.movie.views
        res = self.client.get(f"{BASE_URL}/movies/{self.movie.id}/watch/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.views, views_before + 1)

    def test_watch_movie_not_found(self):
        res = self.client.get(f"{BASE_URL}/movies/999/watch/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_movie(self):
        res = self.client.post(f"{BASE_URL}/movies/{self.movie.id}/like/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_like_movie_not_found(self):
        res = self.client.post(f"{BASE_URL}/movies/999/like/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_dislike_movie_not_found(self):
        res = self.client.post(f"{BASE_URL}/movies/999/dislike/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_rating(self):
        res = self.client.post(f"{BASE_URL}/movies/{self.movie.id}/ratings/", {"score": 5})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_add_comment(self):
        res = self.client.post(f"{BASE_URL}/movies/{self.movie.id}/comments/", {
            "name": "Tester", "content": "Nice!"
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_like_comment(self):
        comment = Comment.objects.create(movie=self.movie, name="Tester", content="Cool!")
        res = self.client.post(f"{BASE_URL}/comments/{comment.id}/like/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_like_comment_not_found(self):
        res = self.client.post(f"{BASE_URL}/comments/999/like/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_dislike_comment_not_found(self):
        res = self.client.post(f"{BASE_URL}/comments/999/dislike/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_genre_without_login_fail(self):
        res = self.client.post(f"{BASE_URL}/genres/", {"name": "Comedy"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_movie_without_admin_fail(self):
        self.authenticate_as("user", "userpass")
        res = self.client.put(f"{BASE_URL}/movies/{self.movie.id}/", {
            "title": "New Title",
            "description": "Updated desc",
            "video_url": "http://example.com/new.mp4",
            "poster_url": "http://example.com/poster.jpg",
            "release_year": 2025,
            "genre_ids": [self.genre.id]
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_movies_by_genre(self):
        res = self.client.get(f"{BASE_URL}/genres/{self.genre.id}/movies/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_average_rating_and_count(self):
        Rating.objects.create(movie=self.movie, score=4)
        Rating.objects.create(movie=self.movie, score=5)
        res = self.client.get(f"{BASE_URL}/movies/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        movie_data = next(m for m in res.json() if m["id"] == self.movie.id)
        self.assertEqual(movie_data["average_rating"], 4.5)
        self.assertEqual(movie_data["rating_count"], 2)
