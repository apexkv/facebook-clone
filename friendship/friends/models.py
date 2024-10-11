from django.db import models
import json
import uuid
from neomodel import (
    StructuredNode,
    StringProperty,
    Relationship,
)
from neomodel import db


def p_print(data):
    p = json.dumps(data, indent=4)
    print(p)


class User(StructuredNode):
    FRIENDS_WITH = "FRIENDS_WITH"
    user_id = StringProperty()
    full_name = StringProperty()

    friends = Relationship("User", FRIENDS_WITH)

    def add_friend(self, user):
        """
        Add a user as a friend if not already friends.
        """
        if not self.is_friends_with(user):
            self.friends.connect(user)
            user.friends.connect(self)

    def is_friends_with(self, user):
        """
        Check if the current user is already friends with another user.
        """
        return self.friends.is_connected(user)

    def remove_friend(self, user):
        """
        Remove a user from friends list.
        """
        if self.is_friends_with(user):
            self.friends.disconnect(user)
            user.friends.disconnect(self)

    def get_friends(self):
        """
        Get all friends of the user.
        """
        return self.friends.all()

    def get_mutual_friends(self, other_user):
        """
        Get mutual friends with another user using a Cypher query.
        """
        query = """
        MATCH (u:User)-[:FRIENDS_WITH]->(mutual:User)<-[:FRIENDS_WITH]-(o:User)
        WHERE u.user_id = $user_id AND o.user_id = $other_user_id
        RETURN mutual
        """

        parameters = {
            "user_id": self.user_id,
            "other_user_id": other_user.user_id,
        }

        results, _ = db.cypher_query(query, parameters)
        # Convert results to User nodes
        mutual_friends = [User.inflate(record[0]) for record in results]

        return mutual_friends

    def __str__(self):
        return self.user_id


class BaseUser(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_to = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="user_to_requests"
    )
    user_from = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="user_from_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_from} -> {self.user_to}"

    def accept(self):
        """
        Accept a friend request.
        """
        user_from = User.nodes.get(user_id=self.user_from.user_id)
        user_to = User.nodes.get(user_id=self.user_to.user_id)

        user_from.add_friend(user_to)

        self.delete()

    def reject(self):
        """
        Reject a friend request.
        """
        self.delete()
