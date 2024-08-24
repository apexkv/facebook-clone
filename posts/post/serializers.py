from rest_framework import serializers
from post.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "full_name", "profile_pic"]


def user_validator(user_id):
    user = User.objects.filter(user_id=user_id)
    if not user.exists():
        raise serializers.ValidationError("User does not exist.")
    return user_id


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True, validators=[user_validator])

    class Meta:
        model = Post
        fields = ["id", "user_id", "content", "user"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.filter(user_id=user_id).first()
        post = Post.objects.create(user=user, **validated_data)
        return post
