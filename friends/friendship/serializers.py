from rest_framework import serializers
from .models import FriendRequest, User


class FriendRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()
    to_user = serializers.UUIDField()

    def cancel(self):
        pass

    def create(self, user):
        pass
