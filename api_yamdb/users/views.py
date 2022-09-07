from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from .serializers import RegisterSerializer
from rest_framework import generics


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from users.models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    email = serializers.EmailField(
    validators=[UniqueValidator(queryset=User.objects.all())]
    )
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
