from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, mixins
import random
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from reviews.models import Categories, Genres, Titles
from rest_framework.decorators import permission_classes, api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from reviews.models import Categories, Genres, Titles, Review, Comments
from users.permissions import NotModerator, IsAdminUserOrReadOnly, IsMyselfOrAdmin
from django.db.models import Avg

from rest_framework.pagination import PageNumberPagination
from django.db import models


from .permissions import (
    AuthorModeratorOrReadOnly,
    IsAdminOrReadOnly,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitlesCreateSerializer,
    TitlesReadSerializer,
    CategoriesSerializer,
    GenresSerializer,
    WriteTitlesSerializer,
    ReadTitlesSerializer,
    UserSignupSerializer,
)
from .paginations import CustomPagination
from .filters import TitlesFilter


@api_view(["POST"])
@permission_classes((IsMyselfOrAdmin,))
def my_review(request):
    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination = PageNumberPagination
    permission_classes = (AuthorModeratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination = PageNumberPagination
    permission_classes = (AuthorModeratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    serializer_class = (TitlesCreateSerializer)
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Выбор сериализатора для необходимого запроса."""
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = WriteTitlesSerializer
    permission_classes = (AuthorModeratorOrReadOnly)
    pagination_class = CustomPagination
    filterset_class = TitlesFilter

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



