from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import UserLoginSerializer, UserSerializer, UserUpdateSerializer
from .models import BaseUser


class UserLoginView(ModelViewSet):
    serializer_class = UserLoginSerializer

    def get_queryset(self) -> BaseUser:
        if "email" in self.request.data:
            return BaseUser.objects.filter(email=self.request.data["email"]).first()
        return BaseUser.objects.all()

    def create(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]
        user = self.get_queryset()

        if not user:
            return Response(
                {
                    "email": "Invalid User Credentials.",
                    "password": "Invalid User Credentials.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(password, user.password):
            return Response(
                {
                    "email": "Invalid User Credentials.",
                    "password": "Invalid User Credentials.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        user.update_lastlogin()

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserView(ModelViewSet):
    def get_serializer_class(self):
        if self.action in ["update"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["update"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action in ["update", "partial_update"]:
            return BaseUser.objects.filter(email=self.request.user.email)
        return BaseUser.objects.all().order_by("full_name")

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        data = serializer.data
        user = BaseUser.objects.get(pk=data["id"])

        refresh = RefreshToken.for_user(user)
        user.update_lastlogin()

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )


class UserMeView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BaseUser.objects.filter(email=self.request.user.email)

    def retrieve(self, request, *args, **kwargs):
        data = self.get_serializer_class()(
                self.request.user, context={"request": request}
            ).data
            
        return Response(data)
