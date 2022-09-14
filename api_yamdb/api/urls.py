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

router.register(r"users", UserViewSet)
router.register(r"categories", CategoriesViewSet)
router.register(r"genres", GenresViewSet)
router.register(r"titles", TitlesViewSet)
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet)
urlpatterns = [
    path("v1/", include(router.urls)),
    url(r"^v1/auth/signup/", signup),
    url("v1/auth/token/", get_token),
]
