from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

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
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("posts/", views.PostViewSet.as_view({"post": "create"})),
    path("users/", views.UsersViewSet.as_view({"get": "list"})),
    path(
        "posts/<uuid:pk>/comments/",
        views.CommentsViewSet.as_view({"post": "create", "get": "list"}),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
