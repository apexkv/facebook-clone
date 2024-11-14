import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch, Exists, OuterRef
from django.db import connection
from datetime import timedelta
from django.conf import settings
import os
import json
import random

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from .serializers import (
    PostSerializer,
    UserSerializer,
    CommentSerializer,
)
from .models import Post, User, Comment, CommentLike, PostLike

posts_created = False


comment_list = [
    {
        "content": "Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis."
    },
    {
        "content": "Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat."
    },
    {
        "content": "Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum."
    },
    {"content": "Nulla ut erat id mauris vulputate elementum. Nullam varius."},
    {
        "content": "Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem."
    },
    {
        "content": "Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum."
    },
    {
        "content": "Morbi a ipsum. Integer a nibh. In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet."
    },
    {
        "content": "Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla."
    },
    {"content": "Sed sagittis."},
    {
        "content": "Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
    },
    {
        "content": "Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat."
    },
    {
        "content": "Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis. Donec semper sapien a libero. Nam dui."
    },
    {
        "content": "Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum."
    },
    {
        "content": "Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero."
    },
    {
        "content": "Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl."
    },
    {
        "content": "Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis."
    },
    {
        "content": "Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis. Sed ante."
    },
    {
        "content": "Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam."
    },
    {
        "content": "Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque."
    },
    {
        "content": "Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus."
    },
]


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

        return (
            Post.objects.select_related("user")
            .filter(user__id=user_id)
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        context = super(UserPostsViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        queryset = Post.objects.filter(user__id=user_id).order_by("-created_at")
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class FeedViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        token = self.request.headers.get("Authorization")
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

        user_ids = [str(friend["user_id"]) for friend in response.json()]

        two_weeks_ago = timezone.now() - timedelta(weeks=2)

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
                    .order_by("-created_at")[:3],
                    to_attr="latest_comments",
                ),
            )
            .filter(user__id__in=user_ids, created_at__gte=two_weeks_ago)
            .order_by("-created_at")
        )

        return queryset

    # @method_decorator(cache_page(60 * 1))  # 1 minuites
    # @method_decorator(vary_on_headers("Authorization"))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(FeedViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
