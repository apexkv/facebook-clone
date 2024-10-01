from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["content"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(user=user, **validated_data)
        return post
