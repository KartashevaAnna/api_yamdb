from rest_framework import generics
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from .permissions import IsMyselfOrAdmin

from .serializers import CustomTokenObtainPairSerializer, UserSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = "username"
    permission_classes = [IsMyselfOrAdmin,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        url_path=r"v1/users/(?P<username>[\w.@+-]+)/$",
        url_name="username page",
    )
    def get_self_page(self, request):
        return self.request.user
