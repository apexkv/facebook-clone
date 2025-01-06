import json
from typing import Dict, List, Literal, TypedDict
from django.db import models
from django.db.models import Count, Q, Subquery, OuterRef
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import User, Message, Room
from .serializers import UserSerializer, MessageSerializer, RoomSerializer


# Event Types
EventTypes = Literal["friend.online", "friend.offline", "chat.message", "friend.typing.start", "friend.typing.stop", "chat.read"]
class ChatMessageType(TypedDict):
    room:str
    content:str
    user: str


# Request Class for Serializers
class Request:
    def __init__(self, user:User):
        self.user = user


class ChatUserConsumer(WebsocketConsumer):
    def connect(self):
        """
        Called when the websocket is handshaking as part of the connection process.
        """
        user:User = self.scope["user"]

        # Check if user is authenticated
        if not user.is_authenticated:
            # Close the connection if user is not authenticated
            return self.close()

        # Accept the connection
        self.accept()
        # Set user online
        user.user_online()
        # Join friendship groups
        self.join_friendship_groups(user)
        # Notify friends that user is online
        self.notify_friends_user_status(user, "friend.online")

    def disconnect(self, close_code):
        user:User = self.scope["user"]
        # Set user offline
        user.user_offline()
        # Notify friends that user is offline
        self.notify_friends_user_status(user, "friend.offline")
        # Leave friendship groups
        self.leave_friendship_groups(user)

    def receive(self, text_data):
        data = json.loads(text_data)

        # Get event type and data
        event_type:EventTypes|None = data.get("type", None)
        event_data = data.get("data", None)

        # Check if event type and data exists
        if event_type and event_data:
            if event_type == "chat.message":
                self.chat_message_send(event_data)
            elif event_type == "friend.typing.start":
                self.friend_start_typing(event_data)
            elif event_type == "friend.typing.stop":
                self.friend_stop_typing(event_data)
            elif event_type == "chat.read":
                self.read_chat(event_data)
            
    
    def sendmessage(self, group_id,type: EventTypes, data:Dict | List):
        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            group_id,
            self.data(type, data)
        )

    def data(self, event_type:EventTypes , data:List|Dict):
        # Create data object
        data = {
            "type": event_type,
            "message": {
                "type": event_type,
                "data": data
            }
        }
        return data

    def join_friendship_groups(self, user:User):
        """
        Join friendship groups
        """
        rooms = Room.objects.filter(users__in=[user])

        for room in rooms:
            async_to_sync(self.channel_layer.group_add)(
                str(room.id),
                self.channel_name
            )
    
    def leave_friendship_groups(self, user:User):
        """
        Leave friendship groups
        """
        rooms = Room.objects.filter(users__in=[user])

        for room in rooms:
            async_to_sync(self.channel_layer.group_discard)(
                str(room.id),
                self.channel_name
            )

    def notify_friends_user_status(self, user:User, status:Literal["friend.online", "friend.offline"]):
        """
        Notify friends that user is online or offline
        """

        if status == "friend.online":
            rooms = (
                Room.objects.annotate(
                    unread_count=Count(
                        "messages",
                        filter=Q(messages__is_read=False) & Q(messages__user=user),
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
        elif status == "friend.offline":
            rooms = (
                Room.objects.annotate(
                    unread_count=Count(
                        "messages",
                        filter=Q(messages__is_read=False) & Q(messages__user=user),
                        distinct=True
                    ),
                    last_message=Subquery(
                        Message.objects.filter(room=OuterRef("pk")).order_by("-created_at").values("content")[:1]
                    )
                )
                .prefetch_related("users")
                .filter(users__in=[user])
                .filter(users__is_online=True)
                .order_by("-last_message_at")
            )
            
        for room in rooms:
            send_user:User = room.users.filter(~Q(id=user.id)).first()
            request = Request(send_user)
            self.sendmessage(str(room.id), status, RoomSerializer(room, context={"request": request}).data)

    def friend_online(self, event):
        """
        Notify user that friend is online
        """
        user = self.scope["user"]
        message = event["message"]
        if str(user.id) != str(message["data"]["friend"]["id"]):
            self.send(text_data=json.dumps(message))
            
    def friend_offline(self, event):
        """
        Notify user that friend is offline
        """
        user = self.scope["user"]
        message = event["message"]
        if str(user.id) != str(message["data"]["friend"]["id"]):
            self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        """
        Notify user that a message has been sent
        """
        data = event["message"]
        user = self.scope["user"]
        if str(user.id) != str(data["data"]["user"]["id"]):
            self.send(text_data=json.dumps(data))

    def chat_message_send(self, event_data:ChatMessageType):
        """
        Send message to chat room
        """
        user = self.scope["user"]
        room_id = event_data.get("room", None)
        content = event_data.get("content", None)

        if not room_id or not content:
            return

        room = Room.objects.filter(id=room_id, users__in=[user])

        if not room.exists():
            if_room_user = User.objects.filter(id=room_id)

            if not if_room_user.exists():
                return
            
            room = Room()
            room.save()
            
            room.users.add(user, if_room_user.first())
        
        other_user = room.first().users.exclude(id=user.id).first()

        message = Message(
            room=room.first(),
            user=user,
            content=content
        )
        message.save()
        room.update(last_message_at=message.created_at)

        self.sendmessage(room_id, "chat.message", MessageSerializer(message, context={"request": Request(other_user)}).data)
        
    
    def friend_start_typing(self, event):
        """
        Send typing start event to chat room
        """
        room_id = event["room"]
        user = self.scope["user"]
        room = Room.objects.filter(id=room_id)

        if not room.exists():
            return
        
        self.sendmessage(room_id, "friend.typing.start", { "room": room_id, "user": str(user.id) })
        

    def friend_stop_typing(self, event):
        """
        Send typing stop event to chat room
        """
        room_id = event["room"]
        user = self.scope["user"]
        room = Room.objects.filter(id=room_id)

        if not room.exists():
            return
        
        self.sendmessage(room_id, "friend.typing.stop", { "room": room_id, "user": str(user.id) })

    def friend_typing_start(self, event):
        """
        Notify user that friend is typing
        """
        user = self.scope["user"]
        message = event["message"]

        if str(user.id) != str(message["data"]["user"]):
            self.send(text_data=json.dumps(message))

    def friend_typing_stop(self, event):
        """
        Notify user that friend has stopped typing
        """
        user = self.scope["user"]
        message = event["message"]

        if str(user.id) != str(message["data"]["user"]):
            self.send(text_data=json.dumps(message))

    def read_chat(self, event):
        """
        Mark messages as read
        """
        user = self.scope["user"]
        room_id = event["room"]

        room = Room.objects.filter(id=room_id, users__in=[user])

        if not room.exists():
            return
        
        room = room.first()
        other_user = room.users.exclude(id=user.id).first()

        messages = Message.objects.filter(room=room, is_read=False, user=other_user)
        messages.update(is_read=True)

        self.sendmessage(room_id, "chat.read", { "room": room_id, "user": str(user.id) })

    def chat_read(self, event):
        """
        Notify user that messages have been read
        """
        user = self.scope["user"]
        message = event["message"]

        if str(user.id) != str(message["data"]["user"]):
            self.send(text_data=json.dumps(message))
