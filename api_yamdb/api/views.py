from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
import random
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from reviews.models import Category, Genre, Title, Review
from users.permissions import (
    IsAdminUserOrReadOnly,
    IsMyselfOrAdmin,
)
from django.db.models import Avg

from rest_framework.pagination import PageNumberPagination

from .permissions import (
    AuthorModeratorOrReadOnly,
    IsAdminOrReadOnly,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    CategorySerializer,
    GenreSerializer,
    WriteTitleSerializer,
    ReadTitleSerializer,
)
from .filters import TitlesFilter


@api_view(["POST"])
@permission_classes((IsMyselfOrAdmin,))
def my_review(request):
    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination = PageNumberPagination
    permission_classes = (AuthorModeratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination = PageNumberPagination
    permission_classes = (AuthorModeratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.annotate(rating=Avg("reviews__score"))
        .all()
        .order_by("name")
    )
    serializer_class = TitleCreateSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Выбор сериализатора для необходимого запроса."""
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
