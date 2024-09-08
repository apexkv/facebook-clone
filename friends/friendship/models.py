from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    UniqueIdProperty,
)


class User(StructuredNode):
    FRIENDS_WITH = "FRIENDS_WITH"
    user_id = StringProperty()
    full_name = StringProperty()
    profile_pic = StringProperty()

    # Define relationship to other users
    friends = RelationshipTo("User", FRIENDS_WITH)

    # Reverse relationship for easy querying
    friends_with = RelationshipFrom("User", FRIENDS_WITH)

    def __str__(self):
        return self.full_name

    def add_friend(self, friend_user, score=0):
        """Add or update a friendship with a score"""
        rel = self.friends.connect(friend_user)
        rel.interaction_score = score
        rel.save()


class FriendRequest(StructuredNode):
    user_from_id = UniqueIdProperty()
    user_to_id = UniqueIdProperty()
