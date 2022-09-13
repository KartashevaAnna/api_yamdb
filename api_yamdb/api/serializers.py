from rest_framework import serializers

from reviews.models import Categories, Genres, Titles, Review, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Titles

class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(
        read_only=True)
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = "__all__"
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Comments
