from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipFrom,
    RelationshipTo,
    IntegerProperty,
    DateTimeProperty,
    Relationship,
)


class User(StructuredNode):
    FRIENDS_WITH = "FRIENDS_WITH"
    user_id = StringProperty()
    full_name = StringProperty()
    profile_pic = StringProperty()

    # Define relationship to other users
    friends = Relationship("User", FRIENDS_WITH)

    def __str__(self):
        return self.full_name

    def add_friend(self, friend_user):
        """Make the friendship bidirectional"""
        # Connect this user to the friend (self -> friend)
        self.friends.connect(friend_user)

    def is_friends_with(self, friend_user):
        """Check if the user is already friends with another user"""
        return self.friends.is_connected(friend_user)


class FriendRequest(StructuredNode):
    SENT_REQUEST = "SENT_REQUEST"
    RECEIVED_REQUEST = "RECEIVED_REQUEST"

    REQUEST_PENDING = 0
    REQUEST_ACCEPTED = 1
    REQUEST_REJECTED = 2

    STATUS_CHOICES = {
        REQUEST_PENDING: "Pending",
        REQUEST_ACCEPTED: "Accepted",
        REQUEST_REJECTED: "Rejected",
    }

    # Relationship from the sender of the friend request
    user_from = RelationshipFrom("User", SENT_REQUEST)

    # Relationship to the recipient of the friend request
    user_to = RelationshipTo("User", RECEIVED_REQUEST)

    created_at = DateTimeProperty(default_now=True)
    status = IntegerProperty(default=REQUEST_PENDING)

    def get_status_display(self):
        """
        Return the human-readable status.
        """
        return self.STATUS_CHOICES.get(self.status, "Unknown")

    def accept(self):
        """
        Accept the friend request and create a FRIENDS_WITH relationship
        """
        if self.status != self.REQUEST_PENDING:
            return False  # Request has already been processed

        try:
            # Retrieve sender and receiver from the relationship
            user_from = self.user_from.single()
            user_to = self.user_to.single()

            if not user_from or not user_to:
                return False  # If either user doesn't exist, fail gracefully

            # Check if they are already friends
            if user_to in user_from.friends or user_from in user_to.friends:
                return False  # They are already friends, no need to re-add

            # Create a mutual friendship
            user_from.add_friend(user_to)
            user_to.add_friend(user_from)

            # Mark the request as accepted
            self.status = self.REQUEST_ACCEPTED
            self.save()
            return True  # Successfully accepted

        except Exception as e:
            # Handle potential errors, like missing users or relationship issues
            print(f"Error accepting friend request: {e}")
            return False  # Operation failed

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
