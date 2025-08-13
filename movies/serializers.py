from rest_framework import serializers
from .models import Movie, Rating, Comment, Genre

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        extra_kwargs = {
            'movie': {'required': False}  
        }

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'movie': {'required': False}  
        }

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

class GenreSerializer(serializers.ModelSerializer):
    # Loại bỏ unique validator mặc định để tránh lỗi khi dùng nested creation
    name = serializers.CharField(validators=[], allow_blank=False)

    class Meta:
        model = Genre
        fields = ['id', 'name']

    def validate_name(self, value):
        # Chuẩn hoá và kiểm tra rỗng
        value = value.strip().title()
        if not value:
            raise serializers.ValidationError("Tên thể loại không được để trống.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    views = serializers.IntegerField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    # Dùng cho input
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        write_only=True,
        required=True,
        allow_empty=False
    )
    # Dùng cho output
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'video_url', 'poster_url',
            'release_year', 'genre_ids', 'genres',
            'average_rating', 'rating_count', 'views', 'likes', 'dislikes'
        ]

    def create(self, validated_data):
        genres = validated_data.pop('genre_ids', [])
        movie = Movie.objects.create(**validated_data)
        movie.genres.set(genres)
        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop('genre_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if genres is not None:
            instance.genres.set(genres)
        return instance
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum([r.score for r in ratings]) / ratings.count(), 1)
        return None

    def get_rating_count(self, obj):
        return obj.ratings.count()