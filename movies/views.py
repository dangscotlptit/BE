from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer

# 🔍 Lấy danh sách phim + tạo mới (chỉ admin)
class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return []

# 🔍 Chi tiết + cập nhật + xoá phim (chỉ admin)
class MovieRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return []

# 🎬 Xem phim
class WatchMovie(generics.RetrieveAPIView):
    queryset = Movie.objects.all()

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)
        return Response({"video_url": movie.video_url})
