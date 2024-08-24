from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated

from post.serializers import PostSerializer
from post.models import Post


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by("created_at")

    @method_decorator(cache_page(1 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
