from rest_framework import status
from neomodel import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest, User
from .serializers import FriendRequestSerializer, UserSerializer


class FriendRequestView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.nodes.all()

    def get_serializer_class(self):
        return FriendRequestSerializer

    def list_sent(self, request, *args, **kwargs):
        """
        Return the list of friend requests sent by the authenticated user.
        """
        user = request.user
        sent_requests = FriendRequest.nodes.filter(user_from=user)

        data = [
            {
                "user_to": UserSerializer(friend_request.user_to.single()).data,
                "id": friend_request.id,
            }
            for friend_request in sent_requests
        ]
        return Response(data, status=status.HTTP_200_OK)

    def list_received(self, request, *args, **kwargs):
        """
        Return the list of friend requests received by the authenticated user.
        """
        user = request.user
        received_requests = FriendRequest.nodes.filter(user_to=user)

        data = [
            {
                "user_from": UserSerializer(friend_request.user_from.single()).data,
                "id": friend_request.id,
            }
            for friend_request in received_requests
        ]
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a friend request from the authenticated user to another user.
        """
        user_from = request.user
        user_to_id = request.data.get("user_to_id")

        try:
            user_to = User.nodes.get(user_id=user_to_id)

            # Check if a friend request already exists in either direction
            existing_request_outgoing = FriendRequest.nodes.filter(
                user_from=user_from, user_to=user_to
            )

            # existing_request_incoming = FriendRequest.nodes.filter(
            #     user_from___contains=user_to, user_to___contains=user_from
            # )

            print("[TXT]", existing_request_outgoing.__dict__)
            print("[TXT]", len(existing_request_outgoing))
            # print("[TXT]", existing_request_incoming)

            # if existing_request_outgoing:
            #     return Response(
            #         {"detail": "Friend request already exists."},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )

            # # Create a new friend request
            # friend_request = FriendRequest()
            # friend_request.user_from.connect(user_from)  # Connect relationship
            # friend_request.user_to.connect(user_to)  # Connect relationship
            # friend_request.save()

            return Response(
                # FriendRequestSerializer(friend_request).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(e)
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a friend request. Either the sender or recipient can cancel it.
        """
        user = request.user
        request_id = kwargs.get("request_id")

        try:
            # Fetch the friend request by ID
            friend_request = FriendRequest.nodes.get(id=request_id)

            # Check if the authenticated user is either the sender or the recipient
            if (
                friend_request.user_from.single() == user
                or friend_request.user_to.single() == user
            ):
                friend_request.delete()
                return Response(
                    {"detail": "Friend request canceled."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"detail": "You do not have permission to cancel this request."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except:
            return Response(
                {"detail": "Friend request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


"""
{
    "user_to_id":"932ac6bd-3d1b-44c1-adbc-71082bafd9bf"
}
"""
