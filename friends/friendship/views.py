from rest_framework.viewsets import ModelViewSet

from friends.friendship.serializers import FriendRequestSerializer, FriendRequest


class FriendRequestView(ModelViewSet):
    def get_serializer_class(self):
        return FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.nodes.all()

    def list_sent(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def list_received(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
