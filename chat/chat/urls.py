from django.contrib import admin
from django.urls import path
from base import views


urlpatterns = [
    path('api/chat/admin/', admin.site.urls),
    path('api/chat/users/', views.ChatUsersView.as_view({"get": "list"})),
    path('api/chat/users/<uuid:pk>/user/', views.ChatUsersView.as_view({"get": "retrieve"})),
    path('api/chat/messages/<uuid:pk>/', views.ChatMessagesView.as_view({"get": "list", "post": "create"})),
]
