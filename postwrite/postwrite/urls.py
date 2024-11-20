from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from posts import views

schema_view = get_schema_view(
    openapi.Info(
        title="FB Clone Posts-Write API",
        default_version="v1",
        description="This handle post create.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kavindu.harshitha97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "api/postwrite/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/postwrite/admin/", admin.site.urls),
    path("api/postwrite/", views.PostViewSet.as_view({"post": "create"})),
    path("api/postwrite/all/", views.PostViewSet.as_view({"get": "list"})),
    path("api/postwrite/users/", views.UsersViewSet.as_view({"get": "list"})),
    path("api/postwrite/feed/", views.FeedViewSet.as_view({"get": "list"})),
    path(
        "api/postwrite/<uuid:pk>/comments/",
        views.CommentsViewSet.as_view({"post": "create", "get": "list"}),
    ),
    path(
        "api/postwrite/users/<uuid:pk>/posts/",
        views.UserPostsViewSet.as_view({"get": "list"}),
    ),
    path(
        "api/postwrite/<uuid:pk>/like/",
        views.PostLikeViewSet.as_view(),
    ),
    path(
        "api/postwrite/comments/<uuid:pk>/like/",
        views.CommentLikeViewSet.as_view(),
    ),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
