from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics
from rest_framework import serializers, exceptions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from .permissions import IsMyselfOrAdmin
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from users.serializers import RegistrationSerializer, TokenSerializer
from rest_framework.authtoken.models import Token


from .serializers import CustomTokenObtainPairSerializer, UserSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def validate(self, attrs):
        data = super().validate(attrs)

        # do your extra validation here
        username_field = User.username
        username = attrs[username_field]
        user = User.objects.get(**{username_field: username})

        if not user.email_verification:
            raise exceptions.AuthenticationFailed(
                {"status": "fail", "message": "verify email"})
        # login(request, user)
        return data

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        url_path=r"v1/users/(?P<username>[\w.@+-]+)/$",
        url_name="username page",
        permission_classes=(IsMyselfOrAdmin,)
    )
    def get_self_page(self, request):
        return self.request.user

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get_or_create(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email')
            )
            confirmation_code = default_token_generator.make_token(request.user)
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                'Код подтверждения для регистрации',
                confirmation_code,
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_token(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = Token.objects.get_or_create(user=request.user)
            send_mail(
                'Тоукен для дальнейших запросов на сайте',
                token,
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
