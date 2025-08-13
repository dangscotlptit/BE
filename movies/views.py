from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Movie, Comment, Rating, Genre
from .serializers import MovieSerializer, CommentSerializer, RatingSerializer, GenreSerializer
from rest_framework.views import APIView

# 🔍 Lấy danh sách phim + tạo mới (chỉ admin)
class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genres__name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return []

# 🔍 Chi tiết + cập nhật + xoá phim (chỉ admin)
class MovieRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return []

# 🎬 Xem phim
class WatchMovie(generics.RetrieveAPIView):
    queryset = Movie.objects.all()

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.views += 1
            movie.save(update_fields=['views'])  # 👁 Tăng lượt xem
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)
        return Response({"video_url": movie.video_url})

class MovieLike(APIView):
    def post(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.likes += 1
            movie.save(update_fields=['likes'])
            return Response({"likes": movie.likes})
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)

class MovieDislike(APIView):
    def post(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.dislikes += 1
            movie.save(update_fields=['dislikes'])
            return Response({"dislikes": movie.dislikes})
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)

class RatingListCreate(generics.ListCreateAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(movie_id=self.kwargs['movie_id'])

    def perform_create(self, serializer):
        serializer.save(movie_id=self.kwargs['movie_id'])

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(movie_id=self.kwargs['movie_id'])

    def perform_create(self, serializer):
        serializer.save(movie_id=self.kwargs['movie_id'])

class CommentLike(APIView):
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.likes += 1
            comment.save(update_fields=['likes'])
            return Response({"likes": comment.likes})
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=404)

class CommentDislike(APIView):
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.dislikes += 1
            comment.save(update_fields=['dislikes'])
            return Response({"dislikes": comment.dislikes})
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=404)

class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


# 📂 API thể loại phim
class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return []

    def create(self, request, *args, **kwargs):
        name = request.data.get("name", "").strip().title()

        if not name:
            raise ValidationError({"error": "Tên thể loại không được để trống."})

        if Genre.objects.filter(name__iexact=name).exists():
            raise ValidationError({"error": f"Thể loại '{name}' đã tồn tại."})

        request.data["name"] = name
        return super().create(request, *args, **kwargs)

class GenreRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        genre = self.get_object()
        if genre.movies.exists():
            raise ValidationError({
                "error": "Không thể xoá thể loại vì đang được sử dụng bởi một hoặc nhiều bộ phim."
            })
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        genre = self.get_object()
        new_name = request.data.get("name", "").strip().title()

        if not new_name:
            raise ValidationError({"error": "Tên thể loại không được để trống."})

        if Genre.objects.exclude(id=genre.id).filter(name__iexact=new_name).exists():
            raise ValidationError({
                "error": f"Thể loại '{new_name}' đã tồn tại. Không thể cập nhật."
            })

        request.data["name"] = new_name
        return super().update(request, *args, **kwargs)
    
class MoviesByGenre(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        return Movie.objects.filter(genres__id=genre_id)