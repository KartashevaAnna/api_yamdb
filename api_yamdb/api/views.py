from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, mixins
from reviews.models import Categories, Genres, Titles, Review
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from reviews.models import Categories, Genres, Titles, Review, Comments
from users.permissions import NotModerator, IsAdminUserOrReadOnly, IsMyselfOrAdmin
from rest_framework.pagination import PageNumberPagination
from django.db import models


from .filters import TitleFilter
from .permissions import (
    OnlyReadOrСhangeAuthorAdminModerator,
    AdminOrReadOnly,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitlesSerializer,
    CategoriesSerializer,
    GenresSerializer,
    WriteTitlesSerializer,
    ReadTitlesSerializer
)
from .paginations import CustomPagination


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
    serializer_class = WriteTitlesSerializer
    permission_classes = (AdminOrReadOnly)
    pagination_class = CustomPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WriteTitlesSerializer
        return ReadTitlesSerializer

    def get_queryset(self):
        new_queryset = Titles.objects.annotate(
            rating=models.Sum(models.F('reviews__score'))
            / models.Count(models.F('reviews'))
        )
        return new_queryset.order_by('name', 'category', '-year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OnlyReadOrСhangeAuthorAdminModerator,)
    pagination_class = CustomPagination

    def get_queryset(self):
        new_queryset = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return new_queryset.reviews.all()

    def perform_create(self, serializer):
        instance = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OnlyReadOrСhangeAuthorAdminModerator,)
    pagination_class = CustomPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = get_object_or_404(
            Review,
            id=review_id,
            title_id=title_id)
        return new_queryset.comments.all()

    def perform_create(self, serializer):
        instance = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=instance)
