import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Prefetch, Exists, OuterRef, Sum, Value, FloatField, F
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .serializers import (
    FeedPostSerializer,
    UserPostSerializer,
    CommentSerializer,
)
from .models import Post, Comment, CommentLike, PostLike, User, Tag


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise NotFound("Post not found")
        return (
            Comment.objects.select_related("user")
            .filter(post=post)
            .order_by("created_at")
        )

    def get_serializer_context(self):
        context = super(CommentsViewSet, self).get_serializer_context()
        context.update({"request": self.request, "post_id": self.kwargs.get("pk")})
        return context
    
    @swagger_auto_schema(
        operation_description="Create a comment",
        request_body=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="List comments",
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostViewSet(ModelViewSet):
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @swagger_auto_schema(
        operation_description="Create a post",
        request_body=UserPostSerializer,
        responses={
            200: UserPostSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserPostsViewSet(ModelViewSet):
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        user = self.request.user
        comments_count_with_post = 1

        all_tags = [tag.name for tag in Tag.objects.all()]

        
    
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
    
    @swagger_auto_schema(
        operation_description="List user posts",
        responses={
            200: UserPostSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FeedViewSet(ModelViewSet):
    serializer_class = FeedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user:User = self.request.user
        token = self.request.headers.get("Authorization")
        
        two_weeks_ago = timezone.now() - timedelta(weeks=48)
        comments_count_with_post = 3

        try:
            response = requests.get(
                f"http://friends:8000/api/friends/users/{str(user.id)}/friends/?pagination=false",
                headers={"Authorization": token},
            )
        except Exception as e:
            print(e)
            raise APIException("Something went wrong please try again later.")

        if response.status_code != 200:
            raise APIException("Something went wrong please try again later.")
        
        tag_scores = user.user_liked_tags.through.objects.filter(
            user=user
        ).values_list('tag_id', 'interaction_count')

        tag_score_map = {tag_id: score for tag_id, score in tag_scores}

        try:
            user_ids = [friend["id"] for friend in response.json()]
        except Exception as e:
            # tag_popularity = (
            #     Tag.objects.annotate(
            #         popularity=Coalesce(Sum(F("post__like_count")), 0)
            #     )
            #     .values("id", "popularity")
            # )
            # tag_popularity_dict = {tag["id"]: tag["popularity"] for tag in tag_popularity}
            queryset = (
                Post.objects.select_related("user")
                .annotate(
                    is_liked=Exists(
                        PostLike.objects.filter(post=OuterRef("pk"), user=user)
                    ),
                    # priority=Coalesce(
                    #     Sum(F("tags__id").map(tag_popularity_dict)), 0
                    # ),
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
                # .order_by("-priority", "?") 
                .order_by("?") 
            )
            return queryset

        queryset = (
            Post.objects.select_related("user")
            .annotate(
                # tag_priority=Coalesce(
                #     Sum(F('tags__id') * Value(tag_score_map.get(F('tags__id'), 0))),
                #     0,
                #     output_field=FloatField()
                # ),
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
            # .order_by("-tag_priority", "-created_at")
            .order_by("-created_at")
        )

        return queryset

    @method_decorator(cache_page(60 * 5))  # 1 minuites
    @method_decorator(vary_on_headers("Authorization"))
    @swagger_auto_schema(
        operation_description="List feed posts",
        responses={
            200: FeedPostSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(FeedViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class PostLikeSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()
    count = serializers.IntegerField()

class PostLikeViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Like or unlike a post",
        responses={
            200: PostLikeSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        post_id = kwargs.get("pk")

        post_like_count, is_liked = PostLike.like_or_unlike_post(user, post_id)

        return Response({"count": post_like_count, "is_liked": is_liked}, status=status.HTTP_200_OK)


class CommentLikeSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()
    count = serializers.IntegerField()


class CommentLikeViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Like or unlike a comment",
        responses={
            200: CommentLikeSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        comment_id = kwargs.get("pk")
        
        comment_like_count, is_liked = CommentLike.like_or_unlike_comment(user, comment_id)

        return Response({"count": comment_like_count, "is_liked": is_liked})