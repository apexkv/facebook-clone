from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404
from .models import BaseUser, FriendRequest


class UserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    full_name = serializers.CharField()


class FriendRequestSerializer(serializers.Serializer):
    user_to_id = serializers.UUIDField(write_only=True)

    id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    user_from = UserSerializer(read_only=True)
    user_to = UserSerializer(read_only=True)

    def create(self, validated_data):
        user_from = self.context["request"].user
        user_from = BaseUser.objects.filter(user_id=user_from.user_id).first()

        user_to = get_object_or_404(BaseUser, user_id=validated_data["user_to_id"])

        if FriendRequest.objects.filter(user_from=user_from, user_to=user_to).exists():
            raise APIException("Friend request already exists")

        if FriendRequest.objects.filter(user_from=user_to, user_to=user_from).exists():
            raise APIException("Friend request already exists")

        if user_from == user_to:
            raise APIException("You cannot send a friend request to yourself")

        try:
            friend_request = FriendRequest(user_from=user_from, user_to=user_to)
            friend_request.save()
        except Exception as e:
            raise APIException(str(e))

        return friend_request


class FriendRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accept", "reject"])
    request_id = serializers.UUIDField()
