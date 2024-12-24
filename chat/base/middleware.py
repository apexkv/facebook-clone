from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from jwt import decode as jwt_decode
from urllib.parse import parse_qs
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from django.conf import settings
from channels.db import database_sync_to_async
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import requests
from .models import User



class AuthMiddleware:
    """Middleware to authenticate user for channels"""

    def __init__(self, app):
        """Initializing the app."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Authenticate the user based on jwt."""
        close_old_connections()
        try:
            # Decode the query string and get token parameter from it.
            token = parse_qs(scope["query_string"].decode("utf8")).get('token', None)[0]
            
            # Decode the token to get the user id from it.
            data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            # Get the user from database based on user id and add it to the scope.
            scope['user'] = await self.get_user(data['user_id'])
        except (TypeError, KeyError, InvalidSignatureError, ExpiredSignatureError, DecodeError):
            # Set the user to Anonymous if token is not valid or expired.
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return AnonymousUser()
        user.is_authenticated = True
        return user


def JWTAuthMiddlewareStack(app):
    """This function wrap channels authentication stack with JWTAuthMiddleware."""
    return AuthMiddleware(AuthMiddlewareStack(app))



class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return AnonymousUser(), token

        auth_service_url = settings.USERS_SERVICE + "/api/users/me/"

        try:
            response = requests.get(auth_service_url, headers={"Authorization": token})
            if response.status_code == 200:
                user_data = response.json()
                return (
                    self.get_user(user_data["id"]),
                    token.split("JWT")[-1],
                )
            else:
                raise AuthenticationFailed("Invalid token")
        except requests.exceptions.RequestException:
            raise AuthenticationFailed("Auth service unavailable")

    def get_user(self, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return AnonymousUser()
        user.is_authenticated = True
        return user
