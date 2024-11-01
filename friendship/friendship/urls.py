from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from friends import views

schema_view = get_schema_view(
    openapi.Info(
        title="FB Clone Users API",
        default_version="v1",
        description="This handle users authentication.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kavindu.harshitha97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("users/", views.UserView.as_view({"get": "list"})),
    path("users/<uuid:pk>/friends/", views.UserView.as_view({"get": "list"})),
    path(
        "users/<uuid:pk>/friends/mutual/",
        views.MutualFriendsView.as_view({"get": "list"}),
    ),
    path(
        "users/friends/requests/",
        views.FriendRequestView.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "users/friends/requests/action/",
        views.FriendRequestActionView.as_view({"post": "create"}),
    ),
    path(
        "users/friends/requests/sent/",
        views.SentFriendRequestView.as_view({"get": "list"}),
    ),
]
