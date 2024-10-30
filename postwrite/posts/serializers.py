from rest_framework import serializers

from .models import Post, User, Comment, PostLike, CommentLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "created_at", "content", "like_count"]

    def create(self, validated_data):
        user = self.context["request"].user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "created_at", "content", "like_count"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(user=user, **validated_data)
        return post
