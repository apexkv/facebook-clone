from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from base import views

schema_view = get_schema_view(
    openapi.Info(
        title="FB Clone Chat API",
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
        "api/chat/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path('api/chat/admin/', admin.site.urls),
    path('api/chat/users/', views.ChatUsersView.as_view({"get": "list"})),
    path('api/chat/users/<uuid:pk>/', views.ChatUsersView.as_view({"get": "retrieve"})),
    path('api/chat/<uuid:pk>/messages/', views.ChatMessagesView.as_view({"get": "list", "post": "create"})),
]
