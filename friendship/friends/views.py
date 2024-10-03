from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest, User
from .serializers import FriendRequestSerializer, SentRequestSerializer, UserSerializer


class FriendRequestView(ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.nodes.filter(user_to=user)


class SentRequestViewSet(ModelViewSet):
    serializer_class = SentRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.nodes.filter(user_from=user)


class FriendsListViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.get_friends()


class MutualFriendsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, user_id):
        authenticated_user = request.user

        other_user = User.nodes.get(user_id=user_id)

        if not other_user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        mutual_friends = authenticated_user.get_mutual_friends(other_user)

        serializer = UserSerializer(mutual_friends, many=True)

        return Response(serializer.data)
