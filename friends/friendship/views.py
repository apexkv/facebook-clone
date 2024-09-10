from rest_framework.viewsets import ModelViewSet

from friends.friendship.serializers import FriendRequestSerializer, FriendRequest


class FriendRequestView(ModelViewSet):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.nodes.all()
