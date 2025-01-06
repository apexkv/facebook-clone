from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from friends import views

schema_view = get_schema_view(
    openapi.Info(
        title="FB Clone Friends API",
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
        "api/friends/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/friends/admin/", admin.site.urls),
    path("api/friends/users/", views.UserView.as_view({"get": "list"})),
    path("api/friends/me/", views.UserMeView.as_view()),
    path("api/friends/suggestions/<str:pk>/", views.FriendSuggestionsView.as_view()),
    path("api/friends/suggestions/", views.FriendSuggestionsView.as_view()),
    path("api/friends/users/<str:pk>/", views.UserView.as_view({"get": "retrieve"})),
    path(
        "api/friends/users/<str:pk>/friends/",
        views.UserView.as_view({"get": "list"}),
    ),
    path(
        "api/friends/users/<str:pk>/friends/mutual/",
        views.MutualFriendsView.as_view({"get": "list"}),
    ),
    path(
        "api/friends/users/friends/requests/",
        views.FriendRequestView.as_view(),
    ),
    path(
        "api/friends/users/friends/requests/action/",
        views.FriendRequestActionView.as_view({"post": "create"}),
    ),
    path(
        "api/friends/users/friends/requests/sent/",
        views.SentFriendRequestView.as_view(),
    ),
]
