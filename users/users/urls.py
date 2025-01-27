from django.contrib import admin
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from userauth import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views


api_info = openapi.Info(
    title="FB Clone Users API",
    default_version="v1",
    description="This handle users authentication.",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="kavindu@apexkv.com"),
    license=openapi.License(name="MIT License", url="../LICENSE"),
)

schema_view = get_schema_view(api_info, public=True)

urlpatterns = [
    path(
        "api/users/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/users/admin/", admin.site.urls),
    re_path(r"api/users/login/?$", views.UserLoginView.as_view({"post": "create"})),
    re_path(
        r"api/users/register/?$",
        views.UserView.as_view({"post": "create"}),
    ),
    path(
        "api/users/<uuid:pk>/",
        views.UserView.as_view({"delete": "destroy", "get": "retrieve"}),
    ),
    re_path(
        r"api/users/update/?$",
        views.UserView.as_view({"put": "update"}),
    ),
    re_path(r"api/users/me/?$", views.UserMeView.as_view({"get": "retrieve"})),
    re_path(r"api/users/refresh/?$", jwt_views.TokenRefreshView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
