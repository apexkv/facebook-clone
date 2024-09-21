from rest_framework import serializers
from .models import FriendRequest, User, models  # Assuming you are using Neo4j models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "full_name", "profile_pic"]


class FriendRequestSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_from = serializers.SerializerMethodField()
    user_to = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    def get_user_from(self, obj):
        user = (
            obj.user_from.single()
        )  # Assuming you're using Neo4j relationship methods
        return UserSerializer(user).data

    def get_user_to(self, obj):
        user = obj.user_to.single()  # Assuming you're using Neo4j relationship methods
        return UserSerializer(user).data

    class Meta:
        fields = ["id", "user_from", "user_to"]

    def create(self, validated_data):
        """
        Create a new FriendRequest in Neo4j.
        """
        user_from = self.context["request"].user  # Get authenticated user
        user_to = validated_data["user_to"]

        # Check if a friend request already exists in either direction
        existing_request = FriendRequest.nodes.get_or_none(
            (models.Q(user_from=user_from) & models.Q(user_to=user_to))
            | (models.Q(user_from=user_to) & models.Q(user_to=user_from))
        )

        if existing_request:
            raise serializers.ValidationError("Friend request already exists.")

        # Create the FriendRequest using Neo4j model methods
        friend_request = FriendRequest(user_from=user_from, user_to=user_to)
        friend_request.save()
        return friend_request
