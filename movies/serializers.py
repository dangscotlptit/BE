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
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'movie': {'required': False}  
        }

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'video_url', 'poster_url',
            'release_year', 'genres', 'average_rating', 'rating_count'
        ]

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        movie = Movie.objects.create(**validated_data)
        for genre in genres_data:
            g, _ = Genre.objects.get_or_create(**genre)
            movie.genres.add(g)
        return movie

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if genres_data is not None:
            instance.genres.clear()
            for genre in genres_data:
                g, _ = Genre.objects.get_or_create(**genre)
                instance.genres.add(g)

        return instance
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum([r.score for r in ratings]) / ratings.count(), 1)
        return None

    def get_rating_count(self, obj):
        return obj.ratings.count()