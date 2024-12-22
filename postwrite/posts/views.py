import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch, Exists, OuterRef
from datetime import timedelta
from django.conf import settings
import os
import json
import uuid

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from .serializers import (
    FeedPostSerializer,
    UserPostSerializer,
    UserSerializer,
    CommentSerializer,
)
from .models import Post, User, Comment, CommentLike, PostLike

posts_created = False


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):

        global posts_created
        if not posts_created:
            data_path = os.path.join(settings.BASE_DIR, "data")
            posts_data = os.path.join(data_path, "posts.json")

            with open(posts_data, "r") as f:
                posts = f.read()
                posts = json.loads(posts)
                print("Post count", len(posts))

                for post in posts:
                    Post.objects.create(**post)
                    print(f"Post {post['id']} created")

                print("Finished post creation.")

        return super().list(request, *args, **kwargs)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise APIException("Post not found")
        return (
            Comment.objects.select_related("user")
            .filter(post=post)
            .order_by("created_at")
        )

    def get_serializer_context(self):
        context = super(CommentsViewSet, self).get_serializer_context()
        context.update({"request": self.request, "post_id": self.kwargs.get("pk")})
        return context


class PostViewSet(ModelViewSet):
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class UserPostsViewSet(ModelViewSet):
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        user = self.request.user
        comments_count_with_post = 1
    
        queryset = (
            Post.objects.select_related("user")
            .annotate(
                is_liked=Exists(
                    PostLike.objects.filter(post=OuterRef("pk"), user=user)
                ),
            )
            .prefetch_related(
                Prefetch(
                    "comment_set",
                    queryset=Comment.objects.select_related("user")
                    .annotate(
                        is_liked=Exists(
                            CommentLike.objects.filter(
                                comment=OuterRef("pk"), user=user
                            )
                        )
                    )
                    .order_by("-created_at")[:comments_count_with_post],
                    to_attr="latest_comments",
                ),
            )
            .filter(user__id=user_id)
            .order_by("-created_at")
        )

        return queryset

    def get_serializer_context(self):
        context = super(UserPostsViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class FeedViewSet(ModelViewSet):
    serializer_class = FeedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        token = self.request.headers.get("Authorization")
        
        two_weeks_ago = timezone.now() - timedelta(weeks=48)
        comments_count_with_post = 3

        try:
            response = requests.get(
                f"http://friendship:8000/api/friendship/users/{str(user.id)}/friends/?pagination=false",
                headers={"Authorization": token},
            )
        except Exception as e:
            print(e)
            raise APIException("Something went wrong please try again later.")

        if response.status_code != 200:
            raise APIException("Something went wrong please try again later.")

        try:
            user_ids = [friend["id"] for friend in response.json()]
        except Exception as e:
            queryset = (
                Post.objects.select_related("user")
                .annotate(
                    is_liked=Exists(
                        PostLike.objects.filter(post=OuterRef("pk"), user=user)
                    ),
                )
                .prefetch_related(
                    Prefetch(
                        "comment_set",
                        queryset=Comment.objects.select_related("user")
                        .annotate(
                            is_liked=Exists(
                                CommentLike.objects.filter(
                                    comment=OuterRef("pk"), user=user
                                )
                            )
                        )
                        .order_by("-created_at")[:comments_count_with_post],
                        to_attr="latest_comments",
                    ),
                )
                .filter(created_at__gte=two_weeks_ago)
                .order_by("?")
            )
            return queryset

        queryset = (
            Post.objects.select_related("user")
            .annotate(
                is_liked=Exists(
                    PostLike.objects.filter(post=OuterRef("pk"), user=user)
                ),
            )
            .prefetch_related(
                Prefetch(
                    "comment_set",
                    queryset=Comment.objects.select_related("user")
                    .annotate(
                        is_liked=Exists(
                            CommentLike.objects.filter(
                                comment=OuterRef("pk"), user=user
                            )
                        )
                    )
                    .order_by("-created_at")[:comments_count_with_post],
                    to_attr="latest_comments",
                ),
            )
            .filter(user__id__in=user_ids, created_at__gte=two_weeks_ago)
            .order_by("-created_at")
        )

        return queryset

    @method_decorator(cache_page(60 * 1))  # 1 minuites
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(FeedViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class PostLikeViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        post_id = kwargs.get("pk")

        post_like_count, is_liked = PostLike.like_or_unlike_post(user, post_id)

        return Response({"count": post_like_count, "is_liked": is_liked})
    
class CommentLikeViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        comment_id = kwargs.get("pk")
        
        comment_like_count, is_liked = CommentLike.like_or_unlike_comment(user, comment_id)

        return Response({"count": comment_like_count, "is_liked": is_liked})