from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet
from users.views import signup, get_token

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router = SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="Reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
urlpatterns = [
    path("v1/", include(router.urls)),
    url(r"^v1/auth/signup/", signup),
    url("v1/auth/token/", get_token),
]
