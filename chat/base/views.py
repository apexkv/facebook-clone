from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q, Subquery, OuterRef
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import User, Message, Room
from .serializers import RoomSerializer, MessageSerializer
          


class ChatUsersView(ModelViewSet):
    """
    View for listing users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        user:User = self.request.user

        filter = self.request.query_params.get("filter", None)

        if filter:
            if filter == "online":
                # Get all online users
                queryset = (
                    Room.objects.annotate(
                        unread_count=Count(
                            "messages",
                            filter=Q(messages__is_read=False) & ~Q(messages__user=user),
                            distinct=True
                        ),
                        last_message=Subquery(
                            Message.objects.filter(room=OuterRef("pk")).order_by("-created_at").values("content")[:1]
                        )
                    )
                    .prefetch_related("users")
                    .filter(users__in=[user])
                    .annotate(
                        user_count=Count("users")
                    )
                    .filter(
                        user_count=Count("users", filter=Q(users__is_online=True))
                    )
                    .order_by("-last_message_at")
                )

        else:
            # get all users
            queryset = Room.objects.annotate(
                unread_count=Count(
                    "messages",
                    filter=Q(messages__is_read=False) & ~Q(messages__user=user),
                    distinct=True
                ),
                last_message=Subquery(
                    Message.objects.filter(room=OuterRef("pk")).order_by("-created_at").values("content")[:1]
                )
            ).prefetch_related("users").filter(users__in=[user]).order_by("-last_message_at").distinct()


        return queryset
    
    def retrieve(self, request, pk=None):
        """
        Get a single user
        """
        user = self.request.user
        room = Room.objects.annotate(
            unread_count=Count(
                "messages",
                filter=Q(messages__is_read=False) & ~Q(messages__user=user)
            ),
            last_message=Subquery(
                Message.objects.filter(room=OuterRef("pk")).order_by("-created_at").values("content")[:1]
            )
        ).prefetch_related("users").filter(id=pk, users__in=[user])

        if room.exists():
            room = room.first()
            serializer = RoomSerializer(room, context={"request": request})
            return Response(serializer.data)
        
        raise NotFound("User not found")
    

class ChatMessagesView(ModelViewSet):
    """
    View for listing and marking them as read
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Get all messages in a room
        """
        user = self.request.user
        room_id = self.request.parser_context["kwargs"].get("pk", None)

        if room_id:
            queryset = Message.objects.select_related("user", "room").filter(room__id=room_id, room__users__in=[user]).order_by("-created_at")
            return queryset
        
        raise NotFound("User not found")
    
    def create(self, request, pk):
        """
        Mark all messages as read
        """
        user = self.request.user
        room_id = pk
        is_mark_read = bool(self.request.query_params.get("mark_read", False))

        room = Room.objects.filter(id=room_id, users__in=[user])

        if is_mark_read:
            if not room.exists():
                raise NotFound("User not found")
            
            room = room.first()
            messages = Message.objects.filter(Q(room=room) & ~Q(user=user) & Q(is_read=False))

            if messages.exists():
                messages.update(is_read=True)
        
        return Response(status=status.HTTP_200_OK)