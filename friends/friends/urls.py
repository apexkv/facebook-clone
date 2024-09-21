from django.contrib import admin
from django.urls import path
from friendship import views
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="FB-Clone API(Friends)",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    # Sent friend requests
    path("requests/sent/", views.FriendRequestView.as_view({"get": "list_sent"})),
    # Received friend requests
    path(
        "requests/received/", views.FriendRequestView.as_view({"get": "list_received"})
    ),
    # Create friend request
    path("requests/", views.FriendRequestView.as_view({"post": "create"})),
    # Delete friend request
    path(
        "requests/<str:request_id>/",
        views.FriendRequestView.as_view({"delete": "destroy"}),
    ),
]
