from django.urls import include, path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import EmailTokenObtainPairView
router = SimpleRouter()

router.register('v1/users', UserViewSet)
urlpatterns = [
    url(r'^v1/auth/signup/', EmailTokenObtainPairView.as_view()),
    # url(r'^v1/auth/refresh_token/', refresh_jwt_token),
    path('', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
