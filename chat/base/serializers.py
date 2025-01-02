import random
from rest_framework import serializers
from .models import User, Message, Room


def generate_colorful_hex_color():
  while True:
    r = random.randint(30, 220)
    g = random.randint(30, 220)
    b = random.randint(30, 220)

    if not (r == g == b): 
      return f"#{r:02x}{g:02x}{b:02x}"



class UserSerializer(serializers.ModelSerializer):
    bg_color = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "full_name", "is_online", "last_seen", "bg_color"]
    
    def get_bg_color(self, obj):
        return generate_colorful_hex_color()


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    direction = serializers.SerializerMethodField()
    room = serializers.CharField(source="room.id")

    class Meta:
        model = Message
        fields = ["id", "user", "content", "created_at", "direction", "is_read", "room"]

    def get_direction(self, obj):
        return "sent" if obj.user.id == self.context["request"].user.id else "received"


class RoomSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField()
    last_message = serializers.CharField()

    class Meta:
        model = Room
        fields = ["id", "friend", "last_message_at", "unread_count", "last_message"]

    def get_friend(self, obj):
        friend = obj.users.exclude(id=self.context["request"].user.id).first()
        return UserSerializer(friend).data
