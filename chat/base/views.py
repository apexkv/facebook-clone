from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User, Friendship
from .serializers import FriendshipSerializer



class ChatUsersView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer
    
    def get_queryset(self):
        user:User = self.request.user
        queryset = Friendship.objects.filter(user=user).select_related("friend").order_by("-friend__is_online")

        return queryset