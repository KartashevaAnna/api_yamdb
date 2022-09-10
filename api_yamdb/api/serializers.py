from rest_framework import serializers

from reviews.models import Categories, Genres, Titles, Review, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Titles

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Review
