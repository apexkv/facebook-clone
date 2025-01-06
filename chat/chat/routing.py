from django.urls import path
from base.consumers import ChatUserConsumer


websocket_urlpatterns = [
    path("api/chat/ws/chat/", ChatUserConsumer.as_asgi()),
]