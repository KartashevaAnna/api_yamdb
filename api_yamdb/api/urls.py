from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import EmailTokenObtainPairView
from users.views import UserViewSet

router = SimpleRouter()

router.register("v1/users", UserViewSet)
urlpatterns = [
    url(r"^v1/auth/signup/", EmailTokenObtainPairView.as_view()),
    path("", include(router.urls)),
    path("v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
