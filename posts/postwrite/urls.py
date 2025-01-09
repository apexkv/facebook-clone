from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from posts import views


api_info = openapi.Info(
    title="FB Clone Posts API",
    default_version="v1",
    description="This handle post related features.",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="kavindu@apexkv.com"),
    license=openapi.License(name="MIT License", url="../LICENSE"),
)

schema_view = get_schema_view(api_info, public=True)

urlpatterns = [
    path(
        "api/posts/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/posts/admin/", admin.site.urls),
    path("api/posts/", views.PostViewSet.as_view({"post": "create"})),
    path("api/posts/feed/", views.FeedViewSet.as_view({"get": "list"})),
    path(
        "api/posts/<uuid:pk>/comments/",
        views.CommentsViewSet.as_view({"post": "create", "get": "list"}),
    ),
    path(
        "api/posts/users/<uuid:pk>/posts/",
        views.UserPostsViewSet.as_view({"get": "list"}),
    ),
    path(
        "api/posts/<uuid:pk>/like/",
        views.PostLikeViewSet.as_view(),
    ),
    path(
        "api/posts/comments/<uuid:pk>/like/",
        views.CommentLikeViewSet.as_view(),
    ),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
