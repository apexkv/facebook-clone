from rest_framework import serializers
from .models import FriendRequest, User


class FriendRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=(("req", "Send Request"), ("can", "Cancel Request"))
    )
    request_id = serializers.UUIDField()
    from_user = serializers.UUIDField()
    to_user = serializers.UUIDField()

    def request(self):
        pass

    def cancel(self):
        pass

    def create(self, user):
        pass
