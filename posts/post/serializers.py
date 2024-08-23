from rest_framework import serializers
from post.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "profile_pic"]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ["id", "content", "user"]
