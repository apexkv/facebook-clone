from typing import List
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import FriendRequest, User, BaseUser
from .serializers import (
    FriendRequestSerializer,
    UserSerializer,
    FriendRequestActionSerializer,
)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs.get("pk", None):
            user = User.nodes.get_or_none(user_id=self.kwargs["pk"])
            if not user:
                raise NotFound("User not found")
            return user.get_friends()
        return User.nodes.all()


class MutualFriendsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        authenticated_user = self.request.user
        other_user = User.nodes.get_or_none(user_id=user_id)
        if not other_user:
            raise NotFound("User not found")
        mutual_friends = authenticated_user.get_mutual_friends(other_user)
        return mutual_friends


class FriendRequestView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(
            user_to__user_id=self.request.user.user_id
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        print(BaseUser.objects.all().order_by("user_id"))
        return super().list(request, *args, **kwargs)


class SentFriendRequestView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(
            user_from__user_id=self.request.user.user_id
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        print(BaseUser.objects.all().order_by("user_id"))
        return super().list(request, *args, **kwargs)


class FriendRequestActionView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestActionSerializer

    def create(self, request):
        serializer = FriendRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_id = serializer.validated_data["request_id"]
        action = serializer.validated_data["action"]

        friend_request = FriendRequest.objects.filter(id=request_id).first()
        if not friend_request:
            raise NotFound("Friend request not found")

        if action == "accept":
            if friend_request.user_to.user_id != request.user.user_id:
                raise NotFound("Friend request not found")
            friend_request.accept()

        if action == "reject":
            if (
                friend_request.user_to == request.user
                or friend_request.user_from == request.user
            ):
                raise NotFound("Friend request not found")
            friend_request.reject()

        return Response(status=status.HTTP_204_NO_CONTENT)
