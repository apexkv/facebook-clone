import time
from django.db import models
import json
import uuid
from neomodel import (
    StructuredNode,
    StringProperty,
    Relationship,
    UniqueIdProperty,
    DateTimeProperty,
)
from neomodel import db


class FriendRequest(StructuredNode):
    SENT_REQUEST = "SENT_REQUEST"
    RECEIVED_REQUEST = "RECEIVED_REQUEST"
    req_id = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)

    user_from = Relationship("User", SENT_REQUEST)
    user_to = Relationship("User", RECEIVED_REQUEST)

    @classmethod
    def get_sent_requests(cls, user):
        """
        Get all sent friend requests.
        """
        query = """
        MATCH (u1:User)-[:SENT_REQUEST]-(friend_request:FriendRequest)-[:RECEIVED_REQUEST]-(u2:User)
        WHERE u1.user_id = $user_id
        RETURN friend_request
        """

        parameters = {"user_id": user.user_id}

        results, _ = db.cypher_query(query, parameters)

        friend_requests = [cls.inflate(record[0]) for record in results]

        return friend_requests

    @classmethod
    def get_recieved_requests(cls, user):
        """
        Get all recieved friend requests.
        """
        query = """
        MATCH (u1:User)-[:RECEIVED_REQUEST]-(friend_request:FriendRequest)-[:SENT_REQUEST]-(u2:User)
        WHERE u1.user_id = $user_id
        RETURN friend_request
        """

        parameters = {"user_id": user.user_id}

        results, _ = db.cypher_query(query, parameters)

        friend_requests = [cls.inflate(record[0]) for record in results]

        return friend_requests

    @classmethod
    def is_request_exists(self, user_from, user_to):
        """
        Check if a friend request already exists.
        """
        query = """
        MATCH (u1:User)-[:SENT_REQUEST]-(friend_request:FriendRequest)-[:RECEIVED_REQUEST]-(u2:User)
        WHERE (u1.user_id = $user_from AND u2.user_id = $user_to) OR (u1.user_id = $user_to AND u2.user_id = $user_from)
        RETURN friend_request
        """
        parameters = {
            "user_from": user_from.user_id,
            "user_to": user_to.user_id,
        }

        results, _ = db.cypher_query(query, parameters)

        return len(results) > 0

    def accept(self):
        """
        Accept a friend request.
        """
        user_from = self.user_from.single()
        user_to = self.user_to.single()
        user_from.add_friend(user_to)

        self.user_from.disconnect(user_from)
        self.user_to.disconnect(user_to)

        self.delete()

    def reject(self):
        """
        Reject a friend request.
        """
        user_from = self.user_from.single()
        user_to = self.user_to.single()
        self.user_from.disconnect(user_from)
        self.user_to.disconnect(user_to)

        self.delete()

    def __str__(self):
        return f"{self.user_from} -> {self.user_to}"


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

    def get_friends_of_friends(self):
        """
        Get friends of friends using a Cypher query.
        """
        query = """
        MATCH (user:User)-[:FRIENDS_WITH]->(friend:User)-[:FRIENDS_WITH]->(friend_of_friend:User)
        WHERE user.user_id = $user_id
        AND NOT (user)-[:FRIENDS_WITH]->(friend_of_friend)
        AND friend_of_friend.user_id <> $user_id
        RETURN DISTINCT friend_of_friend
        """

        parameters = {"user_id": self.user_id}

        results, _ = db.cypher_query(query, parameters)

        friends_of_friends = [User.inflate(record[0]) for record in results]

        return friends_of_friends

    def is_friends_with(self, user):
        """
        Check if the current user is already friends with user.
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
        friends = self.friends.all()
        sorted_friends = sorted(friends, key=lambda friend: friend.full_name)
        return sorted_friends

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

    def send_friend_request(self, user):
        """
        Send a friend request to another user.
        """
        friend_request = FriendRequest()
        friend_request.save()

        friend_request.user_from.connect(self)
        friend_request.user_to.connect(user)

        return friend_request

    def __str__(self):
        return self.user_id


"""
server {
    listen 5612;
    server_name 172.104.49.87;

    location / {
        proxy_pass http://127.0.0.1:5612;  # Your Flask app port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Logs
    access_log /root/logs/flask_app_access.log;
    error_log /root/logs/flask_app_error.log;
}

"""
