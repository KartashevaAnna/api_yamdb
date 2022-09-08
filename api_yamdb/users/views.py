from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination



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
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=["get", "put"],
        url_path=r'v1/users/(?P<username>[\w.@+-]+)/$',
        url_name="username page"
    )
    def get_self_page(self, request):
        return self.request.user
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
