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
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "created_at", "content", "like_count", "is_liked"]

    def create(self, validated_data):
        user = self.context["request"].user
        post_id = self.context["post_id"]

        post = Post.objects.filter(id=post_id).first()
        comment = Comment.objects.create(user=user, post=post, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(source="latest_comments", many=True, read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "created_at",
            "content",
            "like_count",
            "is_liked",
            "comments",
            "is_feed_post",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(user=user, **validated_data)
        return post


class UserPostSerializer(PostSerializer):
    is_feed_post = serializers.BooleanField(read_only=True, default=False)

class FeedPostSerializer(PostSerializer):
    is_feed_post = serializers.BooleanField(read_only=True, default=True)