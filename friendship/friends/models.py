from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    IntegerProperty,
    DateTimeProperty,
    Relationship,
    UniqueIdProperty,
)
from neomodel.exceptions import DoesNotExist
from neomodel import db


class FriendRequest(StructuredNode):
    REQUEST_PENDING = 0
    REQUEST_ACCEPTED = 1
    REQUEST_REJECTED = 2
    STATUS_CHOICES = {
        REQUEST_PENDING: "Pending",
        REQUEST_ACCEPTED: "Accepted",
        REQUEST_REJECTED: "Rejected",
    }
    SENT_REQUEST = "SENT_REQUEST"
    RECEIVED_REQUEST = "RECEIVED_REQUEST"

    # Request details
    req_id = UniqueIdProperty()
    user_from = RelationshipFrom("User", SENT_REQUEST)
    user_to = RelationshipTo("User", RECEIVED_REQUEST)
    created_at = DateTimeProperty(default_now=True)
    status = IntegerProperty(default=REQUEST_PENDING)

    def accept(self):
        """Accept the friend request and create a FRIENDS_WITH relationship"""
        if self.status == self.REQUEST_PENDING:
            user_from = self.user_from.single()
            user_to = self.user_to.single()

            # Prevent creating duplicate friend relationships
            if not user_from.is_friends_with(user_to):
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
                # Delete the request when canceled
                self.delete()
                return True
            else:
                raise ValueError("Only the sender or recipient can cancel this request")
        return False


class User(StructuredNode):
    FRIENDS_WITH = "FRIENDS_WITH"
    user_id = StringProperty()
    full_name = StringProperty()

    # Define relationship to other users
    friends = Relationship("User", FRIENDS_WITH)

    def add_friend(self, user):
        """
        Add a user as a friend if not already friends.
        """
        if not self.is_friends_with(user):
            self.friends.connect(user)

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

    def has_friend_request_from(self, other_user):
        """
        Check if the current user has a pending friend request from another user.
        """
        try:
            # Check for a pending friend request from other_user to self
            friend_request = FriendRequest.nodes.get(
                user_from=other_user, user_to=self, status=FriendRequest.REQUEST_PENDING
            )
            return True
        except DoesNotExist:
            return False

    def has_friend_request_to(self, other_user):
        """
        Check if the current user has sent a pending friend request to another user.
        """
        try:
            # Check for a pending friend request from self to other_user
            friend_request = FriendRequest.nodes.get(
                user_from=self, user_to=other_user, status=FriendRequest.REQUEST_PENDING
            )
            return True
        except DoesNotExist:
            return False

    def send_friend_request(self, other_user):
        """
        Send a friend request to another user, if no request has been sent or received already.
        """
        if self == other_user:
            raise ValueError("You cannot send a friend request to yourself.")

        # Check if a pending friend request already exists
        if self.has_friend_request_to(other_user):
            raise ValueError("You have already sent a friend request to this user.")

        if self.has_friend_request_from(other_user):
            raise ValueError("This user has already sent you a friend request.")

        # Create the friend request
        friend_request = FriendRequest(user_from=self, user_to=other_user)
        friend_request.save()
        return friend_request
