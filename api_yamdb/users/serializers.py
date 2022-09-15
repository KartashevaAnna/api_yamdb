from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ROLE_CHOICES
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f"Email {email} is already taken.")
        return email

    def validate_username(self, username):
        username = username.lower()
        if username == "me":
            raise serializers.ValidationError(
                f'You cannot use "{username}" as username.'
            )
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f"Username {username} is already in use")
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    role = serializers.CharField(default="user", initial="user")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default="user")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
