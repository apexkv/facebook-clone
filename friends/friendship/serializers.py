from rest_framework import serializers
from .models import FriendRequest, User


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = [""]
