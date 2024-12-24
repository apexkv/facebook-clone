from rest_framework import serializers
from .models import User, Friendship, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FriendshipSerializer(serializers.ModelSerializer):
    friend = UserSerializer()
    user = serializers.CharField(source="user.id")
    room = serializers.CharField()

    class Meta:
        model = Friendship
        fields = ["id", "friend", "user", "room"]


class MessageSerializer(serializers.ModelSerializer):
    user_from = UserSerializer()
    user_to = UserSerializer()

    class Meta:
        model = Message
        fields = "__all__"