<<<<<<< HEAD
=======
import datetime as dt
>>>>>>> c9c401a (reviws and comments fix)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

from reviews.models import Categories, Genres, Titles, Review, Comments


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'))
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!')
        return value


class CategoriesSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    class Meta:
        fields = "__all__"
=======
    lookup_field = 'slug'

    class Meta:
        fields = ('name', 'slug')
>>>>>>> c9c401a (reviws and comments fix)
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        lookup_field = "slug"
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Titles


<<<<<<< HEAD
class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = "__all__"
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Comments
=======
class ReadTitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    name = serializers.CharField()
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category',)


class WriteTitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='slug'
    )
    year = serializers.IntegerField()

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs.get('titles_id')

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(default=CurrentTitleDefault(),)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Не более одного комментария для произведения')
            return data
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
>>>>>>> c9c401a (reviws and comments fix)
