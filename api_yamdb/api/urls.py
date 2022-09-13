from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet
from users.views import signup, get_token
from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router = SimpleRouter()

router.register("v1/users", UserViewSet)
router.register(r"v1/categories", CategoriesViewSet)
router.register(r"v1/genres", GenresViewSet)
router.register(r"v1/titles", TitlesViewSet)
router.register(r"v1/r'titles/(?P<title_id>\d+)/reviews", ReviewViewSet)
urlpatterns = [
    url(r"^v1/auth/signup/", signup),
    path("", include(router.urls)),
    path("v1/auth/token/", get_token),
]
