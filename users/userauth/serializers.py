from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import BaseUser


def check_user_exists(email):
    user = BaseUser.objects.filter(email=email)
    if not user.exists():
        raise serializers.ValidationError("Invalid user credentials")


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, validators=[check_user_exists], min_length=5
    )
    password = serializers.CharField(required=True, min_length=8)


def validate_unique_email(email):
    user_exist = BaseUser.objects.filter(email=email).exists()
    if user_exist:
        raise serializers.ValidationError("Email address already exists.")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(validators=[validate_unique_email])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ["id", "email", "full_name", "profile_pic", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["id", "email", "full_name", "profile_pic", "password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"required": False},
            "full_name": {"required": False},
            "profile_pic": {"required": False},
            "password": {"required": False, "write_only": True},
        }

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
