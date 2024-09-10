from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    IntegerProperty,
    DateTimeProperty,
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
    REQUEST_PENDING = 0
    REQUEST_ACCEPTED = 1
    REQUEST_REJECTED = 2
    STATUS_CHOICES = {
        REQUEST_PENDING: "Pending",
        REQUEST_ACCEPTED: "Accepted",
        REQUEST_REJECTED: "Rejected",
    }

    # Request details
    user_from = RelationshipFrom("User", "SENT_REQUEST")
    user_to = RelationshipTo("User", "RECEIVED_REQUEST")
    created_at = DateTimeProperty(default_now=True)
    status = IntegerProperty(default=REQUEST_PENDING)

    def accept(self):
        """Accept the friend request and create a FRIENDS_WITH relationship"""
        if self.status == self.REQUEST_PENDING:
            user_from = self.user_from.single()
            user_to = self.user_to.single()

            # Create friendship relationship between the two users
            user_from.add_friend(user_to)
            user_to.add_friend(user_from)

            # Update status to accepted
            self.status = self.REQUEST_ACCEPTED
            self.save()

    def cancel(self, canceling_user):
        """
        Cancel the friend request. Either the sender (user_from) or the receiver (user_to) can cancel it.
        """
        if self.status == self.REQUEST_PENDING:
            user_from = self.user_from.single()
            user_to = self.user_to.single()

            # Allow either the sender or recipient to cancel
            if canceling_user == user_from or canceling_user == user_to:
                # Delete the request or mark it as canceled
                self.delete()
                return True
            else:
                return False
        return False
