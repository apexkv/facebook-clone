from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from userauth import views
from rest_framework_simplejwt import views as jwt_views

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )


schema_view = get_schema_view(
    openapi.Info(
        title="FB-Clone API(Users)",
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
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    #
    # path(r"^api/auth/", include("djoser.urls")),
    #
    re_path(r"api/user/login/?$", views.UserLoginView.as_view({"post": "create"})),
    re_path(r"api/user/register/?$", views.UserView.as_view({"post": "create"})),
    re_path(
        r"api/user/update/?$",
        views.UserView.as_view({"put": "update"}),
    ),
    re_path(r"api/user/me/?$", views.UserMeView.as_view({"get": "retrieve"})),
    re_path(r"api/user/refresh/?$", jwt_views.TokenRefreshView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
