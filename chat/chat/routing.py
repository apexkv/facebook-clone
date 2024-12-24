from django.urls import path
from base.consumers import ChatUserConsumer


websocket_urlpatterns = [
    path("api/ws/chat/", ChatUserConsumer.as_asgi()),
]