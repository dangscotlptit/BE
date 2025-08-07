from rest_framework import serializers
from .models import Movie, Rating, Comment

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


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'video_url', 'poster_url', 'release_year', 'average_rating', 'rating_count']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum([r.score for r in ratings]) / ratings.count(), 1)
        return None

    def get_rating_count(self, obj):
        return obj.ratings.count()

