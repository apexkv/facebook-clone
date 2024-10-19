from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import FriendRequest, User


class UserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    full_name = serializers.CharField()


class FriendRequestSerializer(serializers.Serializer):
    user_to_id = serializers.UUIDField(write_only=True)

    req_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["user_from"] = UserSerializer(instance.user_from.single()).data
        rep["user_to"] = UserSerializer(instance.user_to.single()).data

        return rep

    def create(self, validated_data):
        user_from = self.context["request"].user

        user_to = User.nodes.get_or_none(user_id=validated_data["user_to_id"])

        if not user_to:
            raise APIException("User not found")

        if user_from.is_friends_with(user_to):
            raise APIException("Users are already friends")

        if user_from == user_to:
            raise APIException("You cannot send a friend request to yourself")

        if FriendRequest.is_request_exists(user_from, user_to):
            raise APIException("Friend request already exists")

        try:
            friend_request = user_from.send_friend_request(user_to)
        except Exception as e:
            print(e)
            raise APIException(str(e))

        return friend_request


class FriendRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accept", "reject"])
    request_id = serializers.UUIDField()
