import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.db import connection
from django.utils import timezone
from datetime import timedelta

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from .serializers import (
    PostSerializer,
    UserSerializer,
    User,
    Post,
    Comment,
    CommentSerializer,
)


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return Comment.objects.filter(id=post_id).order_by("created_at")

    def get_serializer_context(self):
        context = super(CommentsViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class UserPostsViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("pk")

        # with connection.cursor() as cursor:
        #     query = """
        #     UPDATE posts_post
        #     SET created_at = NOW() - INTERVAL FLOOR(RAND() * (3 * 7 * 24 * 60 * 60)) SECOND;
        #     """
        #     cursor.execute(query)
        #     cursor.execute("SELECT * FROM posts_post LIMIT 10")
        #     result = cursor.fetchall()
        #     print(result)

        return (
            Post.objects.select_related("user")
            .filter(user__id=user_id)
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        context = super(UserPostsViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class FeedViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        token = self.request.headers.get("Authorization")
        try:
            response = requests.get(
                f"http://friendship:8000/users/{user.id}/friends/?pagination=false",
                headers={"Authorization": token},
            )
        except Exception as e:
            print(e)
            raise APIException("Something went wrong please try again later.")

        if response.status_code != 200:
            raise APIException("Something went wrong please try again later.")

        user_ids = [friend["user_id"] for friend in response.json()]

        two_weeks_ago = timezone.now() - timedelta(weeks=2)

        return (
            Post.objects.select_related("user")
            .filter(user__id__in=user_ids, created_at__gte=two_weeks_ago)
            .order_by("-created_at")
        )

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(FeedViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
