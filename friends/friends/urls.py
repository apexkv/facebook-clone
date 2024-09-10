from django.contrib import admin
from django.urls import path
from friendship import views


urlpatterns = [
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
