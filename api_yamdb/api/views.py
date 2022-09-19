from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from reviews.models import Categories, Genres, Titles, Review
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from reviews.models import Categories, Genres, Titles, Review, Comments
from users.permissions import NotModerator, IsAdminUserOrReadOnly, IsMyselfOrAdmin

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentsSerializer,
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ("slug",)
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsMyselfOrAdmin,
    ]
    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())




class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
