from rest_framework import serializers
from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username", "email"]


class FriendRequestSerializer(serializers.ModelSerializer):
    user_from = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["user_from", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        validated_data["status"] = FriendRequest.REQUEST_PENDING
        return super().create(validated_data)


class SentRequestSerializer(serializers.ModelSerializer):
    user_to = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["user_to", "created_at"]
        read_only_fields = ["created_at"]
