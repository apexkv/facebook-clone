import random
from re import A
from typing import List
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import FriendRequest, User
from .serializers import (
    FriendRequestSerializer,
    FriendSuggestionsSerializer,
    UserSerializer,
    FriendRequestActionSerializer,
)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs.get("pk", None):
            user = User.nodes.get_or_none(
                user_id=str(self.kwargs["pk"]).replace("-", "")
            )
            if not user:
                raise NotFound("User not found")
            return user.get_friends()
        return User.nodes.all()
    
    def retrieve(self, request, *args, **kwargs):
        friend_id = str(kwargs["pk"]).replace("-", "")
        user = request.user
        result = user.get_user_by_id(friend_id)

        if not result:
            raise NotFound("User not found")
        
        return Response(result)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        pagination = request.query_params.get("pagination", None)

        if pagination and pagination == "false":
            serializer = self.get_serializer(queryset, many=True)

        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class MutualFriendsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        authenticated_user = self.request.user
        other_user = User.nodes.get_or_none(user_id=user_id)
        if not other_user:
            raise NotFound("User not found")
        mutual_friends = authenticated_user.get_mutual_friends(other_user)
        return mutual_friends


class FriendRequestView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.get_recieved_requests(self.request.user)


class SentFriendRequestView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.get_sent_requests(self.request.user)


class FriendRequestActionView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestActionSerializer

    def create(self, request):
        serializer = FriendRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_id = str(serializer.validated_data["request_id"]).replace("-", "")
        action = serializer.validated_data["action"]

        friend_request = FriendRequest.nodes.get_or_none(req_id=request_id)

        if not friend_request:
            raise NotFound("Friend request not found")

        if action == "accept":
            if friend_request.user_to.single().user_id != request.user.user_id:
                raise NotFound("Friend request not found")
            friend_request.accept()

        if action == "reject":
            if (
                friend_request.user_to == request.user
                or friend_request.user_from == request.user
            ):
                raise NotFound("Friend request not found")
            friend_request.reject()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendSuggestionsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSuggestionsSerializer

    def get(self, request):
        page_number = int(request.query_params.get("page", 1))

        max_result_count = 200
        page_per_result = 10

        result = self.get_suggesion_friends_list()
        base_link = self.request.build_absolute_uri().split("?")[0]
        next_link = f"{base_link}?page={page_number + 1}"
        max_page_number = max_result_count // page_per_result
        

        data = {
            "next": next_link if page_number < max_page_number else None,
            "results": result,
        }

        return Response(data)
    
    def get_suggesion_friends_list(self):
        user = self.request.user
        page_number = int(self.request.query_params.get("page", 1))
        cache_key = f"friend_suggesion_{user.user_id}"
        result = cache.get(cache_key)

        if not result:
            result = user.get_friend_suggesion() 
            random.shuffle(result)
            cache.set(cache_key, result, 60*60*24) # 24 hours
        return_result = result[(page_number - 1) * 10 : page_number * 10]
        return return_result
    
    def delete(self, request, pk):
        cache_key = f"friend_suggesion_{request.user.user_id}"
        user_id = pk

        if not user_id:
            raise NotFound("User not found")
        
        result = cache.get(cache_key)

        if not result:
            raise NotFound("User not found")
        
        result = [user for user in result if user["id"] != user_id]
        ttl = cache.ttl(cache_key)

        if ttl:
            cache.set(cache_key, result, ttl)
        else:
            cache.set(cache_key, result, 60*60*24)

        return Response(status=status.HTTP_204_NO_CONTENT)