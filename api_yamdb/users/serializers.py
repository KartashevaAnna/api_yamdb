from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ROLE_CHOICES
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = "__all__"


class TokenSerializer(serializers.Serializer):
       username = serializers.CharField(required=True)
       confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = "__all__"
