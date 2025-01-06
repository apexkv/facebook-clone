import uuid
from rest_framework import serializers
from django.core.cache import cache
from rest_framework.exceptions import APIException
from .models import FriendRequest, User


class UserSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    full_name = serializers.CharField()
    is_friend = serializers.BooleanField(read_only=True)
    sent_request = serializers.BooleanField(read_only=True)
    received_request = serializers.BooleanField(read_only=True)

    def get_id(self, obj):
        return str(uuid.UUID(obj.user_id))
    

class FriendSuggestionsSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    is_friend = serializers.BooleanField(read_only=True)
    sent_request = serializers.BooleanField(read_only=True)
    received_request = serializers.BooleanField(read_only=True)
    mutual_friends = serializers.IntegerField(read_only=True)
    mutual_friends_list = UserSerializer(many=True, read_only=True)
    mutual_friends_name_list = serializers.ListField(read_only=True)


def update_cache_for_user_suggestions(user_from_id, user_to_id):
    cache_key = f"friend_suggesion_{user_from_id}"
    get_cache = cache.get(cache_key)
    if get_cache:
        cache_ttl = cache.ttl(cache_key)
        arr = []
        for user in get_cache:
            if user["id"].replace("-", "") == user_to_id:
                user["sent_request"] = True
            arr.append(user)
        cache.set(cache_key, arr, timeout=cache_ttl)   


class FriendRequestSerializer(serializers.Serializer):
    user_to_id = serializers.UUIDField(write_only=True)

    req_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    mutual_friends_count = serializers.IntegerField(read_only=True)
    mutual_friends_name_list = serializers.ListField(read_only=True)

    def create(self, validated_data):
        user_from = self.context["request"].user

        user_to = User.nodes.get_or_none(
            user_id=str(validated_data["user_to_id"]).replace("-", "")
        )             

        if not user_to:
            raise APIException("User not found")

        if user_from.is_friends_with(user_to):
            raise APIException("Users are already friends")

        if user_from == user_to:
            raise APIException("You cannot send a friend request to yourself")

        if FriendRequest.is_request_exists(user_from, user_to):
            get_request = FriendRequest.get_request_if_it_available(user_from.user_id, user_to.user_id)
            if get_request:
                update_cache_for_user_suggestions(user_from.user_id, user_to.user_id)
            return get_request

        try:
            friend_request = user_from.send_friend_request(user_to)
        except Exception as e:
            raise APIException(str(e))

        update_cache_for_user_suggestions(user_from.user_id, user_to.user_id)
        return friend_request


class FriendRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accept", "reject"])
    request_id = serializers.UUIDField()
