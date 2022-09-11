from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet
from users.views import signup, get_token

router = SimpleRouter()

router.register("v1/users", UserViewSet)
urlpatterns = [
    url(r"^v1/auth/signup/", signup),
    path("", include(router.urls)),
    path("v1/auth/token/", get_token),
]
