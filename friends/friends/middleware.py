import uuid
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import requests

from .models import User


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
        """
        Retrieve or create a Neo4j user instance based on the user data from the external service.
        """
        user_id = str(user_id).replace("-", "")
        user = User.nodes.get_or_none(user_id=user_id)
        if not user:
            return AnonymousUser()
        user.is_authenticated = True
        return user
