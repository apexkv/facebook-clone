from apexmq.consumers import BaseConsumer
from .models import User


class UserConsumer(BaseConsumer):
    lookup_prefix = "user"

    def created(self, data):
        user = User(
            user_id=data["id"],
            full_name=["full_name"],
        )
        user.save()
        print(user)
        print("User created")
