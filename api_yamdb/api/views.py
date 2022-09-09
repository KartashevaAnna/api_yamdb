from rest_framework import viewsets
from reviews.models import Categories, Genres, Titles
from users.permissions import NotModerator, IsAdminUserOrReadOnly

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer
)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [
        NotModerator,
    ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]
