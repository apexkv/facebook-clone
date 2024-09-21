from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import requests

from friendship.models import User


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return None

        auth_service_url = settings.USERS_SERVICE + "/api/user/me/"

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
        user = User.nodes.get(user_id=user_id)
        user.is_authenticated = True
        print(user)
        return user
