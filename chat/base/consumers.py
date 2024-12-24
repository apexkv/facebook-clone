import json
from typing import Dict, List, Literal
from django.db import models
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import User, Friendship, Message
from .serializers import UserSerializer, FriendshipSerializer, MessageSerializer


EventTypes = Literal["friend.online", "friend.offline", "chat.message"]


class ChatUserConsumer(WebsocketConsumer):
    def connect(self):
        user:User = self.scope["user"]

        if not user.is_authenticated:
            return self.close()

        self.accept()
        user.user_online()
        self.join_friendship_groups(user)
        self.notify_friends_user_status(user, "friend.online")

    def disconnect(self, close_code):
        user:User = self.scope["user"]
        user.user_offline()
        self.notify_friends_user_status(user, "friend.offline")
        self.leave_friendship_groups(user)
    
    def sendmessage(self, group_id,type: EventTypes, data:Dict | List):
        async_to_sync(self.channel_layer.group_send)(
            group_id,
            self.data(type, data)
        )

    def data(self, event_type:EventTypes , data:List|Dict):
        data = {
            "type": event_type,
            "message": {
                "type": event_type,
                "data": data
            }
        }
        return data

    def join_friendship_groups(self, user:User):
        friends = Friendship.objects.filter(user=user)

        for friend in friends:
            async_to_sync(self.channel_layer.group_add)(
                str(friend.room),
                self.channel_name
            )
    
    def leave_friendship_groups(self, user:User):
        friends = Friendship.objects.filter(user=user)

        for friend in friends:
            async_to_sync(self.channel_layer.group_discard)(
                str(friend.room),
                self.channel_name
            )

    def notify_friends_user_status(self, user:User, status:Literal["friend.online", "friend.offline"]):
        friends = Friendship.objects.filter(friend=user, user__is_online=True)

        for friend in friends:
            self.sendmessage(str(friend.room), status, FriendshipSerializer(friend).data)

    def friend_online(self, event):
        user = self.scope["user"]
        message = event["message"]
        if str(user.id) != str(message["data"]["friend"]["id"]):
            self.send(text_data=json.dumps(message))
            
    def friend_offline(self, event):
        user = self.scope["user"]
        message = event["message"]
        if str(user.id) != str(message["data"]["friend"]["id"]):
            self.send(text_data=json.dumps(message))