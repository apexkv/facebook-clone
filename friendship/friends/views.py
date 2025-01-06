import json
import random
from re import A
from typing import List
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.core.cache import cache
from django.utils import timezone
from .models import FriendRequest, User
from friendship.producers import publish
from .serializers import (
    FriendRequestSerializer,
    FriendSuggestionsSerializer,
    UserSerializer,
    FriendRequestActionSerializer,
)


HR_1 = 60 * 60
PAGE_SIZE = 10


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "request_count": user.get_request_count(),
        }
        return Response(user_data, status=status.HTTP_200_OK)


class UserView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        friend_id = str(kwargs["pk"]).replace("-", "")
        user = request.user
        result = user.get_user_by_id(friend_id)

        if not result:
            raise NotFound("User not found")
        
        return Response(result)

    def list(self, request, *args, **kwargs):
        auth_user = request.user
        pagination_enabled = request.query_params.get("pagination", "true") == "true"
        user_id = str(kwargs["pk"]).replace("-", "")
        user = User.nodes.get_or_none(user_id=user_id)

        if not user:
            raise NotFound("User not found")
        
        page_no = int(request.query_params.get("page", 1))
        base_link = self.request.build_absolute_uri().split("?")[0]

        cache_key = f"friend_list_{user_id}"
        cache.delete(cache_key)
        result = cache.get(cache_key)

        if not result:
            result = user.get_friends(auth_user.user_id)
            cache.set(cache_key, result, HR_1)

        next_link = f"{base_link}?page={page_no + 1}"
        max_page_number = len(result) // PAGE_SIZE

        data = {
            "next": next_link if page_no < max_page_number else None,
            "results": result[(page_no - 1) * PAGE_SIZE : page_no * PAGE_SIZE],
        }

        return Response(data if pagination_enabled else result)


class MutualFriendsView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        auth_user = request.user
        user_id = str(kwargs["pk"]).replace("-", "")
        user = User.nodes.get_or_none(user_id=user_id)

        if not user:
            raise NotFound("User not found")
        
        page_no = int(request.query_params.get("page", 1))
        base_link = self.request.build_absolute_uri().split("?")[0]

        cache_key = f"mutual_friend_{user_id}-{auth_user.user_id}"
        cache_key_reverse = f"mutual_friend_{auth_user.user_id}-{user_id}"
        result = cache.get(cache_key) or cache.get(cache_key_reverse)

        if not result:
            result = user.get_mutual_friends(auth_user.user_id)
            cache.set(cache_key, result, HR_1)
            cache.set(cache_key_reverse, result, HR_1)

        next_link = f"{base_link}?page={page_no + 1}"
        max_page_number = len(result) // PAGE_SIZE

        data = {
            "next": next_link if page_no < max_page_number else None,
            "results": result[(page_no - 1) * PAGE_SIZE : page_no * PAGE_SIZE],
        }

        return Response(data)

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    
    def get(self, request, *args, **kwargs):
        page_no = int(request.query_params.get("page", 1))
        base_link = self.request.build_absolute_uri().split("?")[0]

        cache_key = f"friend_request_{request.user.user_id}"
        result = cache.get(cache_key)

        if not result:
            result = FriendRequest.get_recieved_requests(self.request.user)
            cache.set(cache_key, result, HR_1)

        next_link = f"{base_link}?page={page_no + 1}"
        max_page_number = len(result) // PAGE_SIZE

        data = {
            "next": next_link if page_no < max_page_number else None,
            "results": result[(page_no - 1) * PAGE_SIZE : page_no * PAGE_SIZE],
        }

        return Response(data)
    
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        friend_request = serializer.save()
        
        new_friend_request = {
            "req_id": friend_request["req_id"],
            "id": friend_request["user_to"]["id"],
            "full_name": friend_request["user_to"]["full_name"],
            "created_at": friend_request["created_at"].timestamp(),
            "received_request": False,
            "sent_request": False,
            "mutual_friends_count": friend_request["mutual_friends_count"],
            "mutual_friends_name_list": friend_request["mutual_friends_name_list"],
        }

        if friend_request["user_to"]["id"] == str(uuid.UUID(request.user.user_id)):
            new_friend_request["received_request"] = True
        
        if friend_request["user_from"]["id"] == str(uuid.UUID(request.user.user_id)):
            new_friend_request["sent_request"] = True

        cache_key = f"friend_request_{request.user.user_id}"
        cache_result = cache.get(cache_key)

        if cache_result:
            cache_ttl = cache.ttl(cache_key)
            cache_result.insert(0, friend_request)
            cache.set(cache_key, cache_result, timeout=cache_ttl)

        return Response(new_friend_request, status=status.HTTP_201_CREATED)


class SentFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_no = int(request.query_params.get("page", 1))
        base_link = self.request.build_absolute_uri().split("?")[0]

        cache_key = f"sent_friend_request_{request.user.user_id}"
        result = cache.get(cache_key)

        if not result:
            result = FriendRequest.get_sent_requests(self.request.user)
            cache.set(cache_key, result, HR_1)
        
        next_link = f"{base_link}?page={page_no + 1}"
        max_page_number = len(result) // PAGE_SIZE
        print(max_page_number)
        data = {
            "next": next_link if page_no < max_page_number else None,
            "results": result[(page_no - 1) * PAGE_SIZE : page_no * PAGE_SIZE],
        }

        return Response(data)


class FriendRequestActionView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestActionSerializer

    def create(self, request):
        serializer = FriendRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_id = str(serializer.validated_data["request_id"]).replace("-", "")
        action = serializer.validated_data["action"]

        friend_request = FriendRequest.nodes.get_or_none(req_id=request_id)
        action_happened = False

        if not friend_request:
            raise NotFound("Friend request not found")

        if action == "accept":
            if friend_request.user_to.single().user_id != request.user.user_id:
                raise NotFound("Friend request not found")
            friend_request.accept()
            action_happened = True
            data = {
                "friends": [
                    {
                        "id": friend_request.user_from.single().user_id,
                        "full_name": friend_request.user_from.single().full_name,
                    },
                    {
                        "id": friend_request.user_to.single().user_id,
                        "full_name": friend_request.user_to.single().full_name,
                    },
                ]
            }
            publish("friend.created", data, ["chat"])

        elif action == "reject":
            if (
                friend_request.user_to == request.user
                or friend_request.user_from == request.user
            ):
                raise NotFound("Friend request not found")
            friend_request.reject()
            action_happened = True

        if action_happened:
            self.remove_request_from_sent_cache(request_id, request.user.user_id)
            self.remove_request_from_received_cache(request_id, request.user.user_id)            

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def remove_request_from_sent_cache(self, request_id, user_id):
        cache_key = f"sent_friend_request_{user_id}"
        cache_result = cache.get(cache_key)
        if cache_result:
            cache_ttl = cache.ttl(cache_key)
            cache_result = [req for req in cache_result if req["req_id"] != request_id]
            cache.set(cache_key, cache_result, timeout=cache_ttl)
        
    def remove_request_from_received_cache(self, request_id, user_id):
        cache_key = f"friend_request_{user_id}"
        cache_result = cache.get(cache_key)
        if cache_result:
            cache_ttl = cache.ttl(cache_key)
            cache_result = [req for req in cache_result if req["req_id"] != request_id]
            cache.set(cache_key, cache_result, timeout=cache_ttl)


class FriendSuggestionsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSuggestionsSerializer

    def get(self, request):
        page_number = int(request.query_params.get("page", 1))

        max_result_count = 200

        result = self.get_suggesion_friends_list()
        base_link = self.request.build_absolute_uri().split("?")[0]
        next_link = f"{base_link}?page={page_number + 1}"
        max_page_number = max_result_count // PAGE_SIZE
        

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
            cache.set(cache_key, result, HR_1*24) # 24 hours
        return_result = result[(page_number - 1) * PAGE_SIZE : page_number * PAGE_SIZE]
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
            cache.set(cache_key, result, HR_1*24)

        return Response(status=status.HTTP_204_NO_CONTENT)