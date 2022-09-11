from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.serializers import (
    RegistrationSerializer,
    TokenSerializer,
    UserSerializer
)

from .permissions import IsMyselfOrAdmin


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
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get", "put", "patch", "post"],
        url_path=r"v1/users/(?P<username>[\w.@+-]+)/$",
        url_name="username page",
        permission_classes=(IsMyselfOrAdmin,)
    )
    def get_self_page(self, request):
        return self.request.user


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get_or_create(
        username=serializer.validated_data.get('username'),
        email=serializer.validated_data.get('email')
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения для регистрации',
        confirmation_code,
        'from@example.com',
        [request.user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        username = serializer.validated_data.get('username')
        token = Token.objects.get_or_create(user=request.user)
        if default_token_generator.check_token(
                user,
                serializer.validated_data.get('confirmation_code')
        ):
            token = AccessToken.for_user(user)
        send_mail(
            'Тоукен для дальнейших запросов на сайте',
            token,
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
