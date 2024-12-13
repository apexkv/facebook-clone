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
    def get_request_if_it_available(cls, user_from_id, user_to_id):
        """
        Get friend request is it from or to the user.
        """
        query = """
        MATCH (u1:User)-[:SENT_REQUEST]-(friend_request:FriendRequest)-[:RECEIVED_REQUEST]-(u2:User)
        WHERE u1.user_id = $user_from_id AND u2.user_id = $user_to_id OR u1.user_id = $user_to_id AND u2.user_id = $user_from_id
        RETURN friend_request
        """

        parameters = {
            "user_from_id": user_from_id,
            "user_to_id": user_to_id,
        }

        results, _ = db.cypher_query(query, parameters)

        if results:
            return cls.inflate(results[0][0])

        return None

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
        WHERE (u1.user_id = $user_from AND u2.user_id = $user_to)
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

    def get_user_by_id(self, friend_id):
        """
        Get user by user_id with a Cypher query. and need to return result like this
        user_id, full_name, is_friend
        """

        query = """
        MATCH (user:User {user_id: $current_user_id})
        MATCH (friend:User {user_id: $friend_id})
        OPTIONAL MATCH (user)-[:FRIENDS_WITH]-(friend)
        OPTIONAL MATCH (user)-[:SENT_REQUEST]-(request:FriendRequest)-[:RECEIVED_REQUEST]-(friend)
        OPTIONAL MATCH (user)-[:RECEIVED_REQUEST]-(request:FriendRequest)-[:SENT_REQUEST]-(friend)
        RETURN 
        friend.user_id AS user_id, 
        friend.full_name AS full_name, 
        CASE WHEN (user)-[:FRIENDS_WITH]-(friend) THEN true ELSE false END AS is_friend,
        CASE WHEN (user)-[:SENT_REQUEST]-(:FriendRequest)-[:RECEIVED_REQUEST]-(friend) THEN true ELSE false END AS sent_request,
        CASE WHEN (user)-[:RECEIVED_REQUEST]-(:FriendRequest)-[:SENT_REQUEST]-(friend) THEN true ELSE false END AS received_request
        """

        parameters = {
            "current_user_id": self.user_id,
            "friend_id": friend_id,
        }

        results, _ = db.cypher_query(query, parameters)

        if results:
            result = results[0]
            return {
                "id": str(uuid.UUID(str(result[0]))),
                "full_name": result[1],
                "is_friend": result[2],
                "sent_request": result[3],
                "received_request": result[4],
            }

        return None
        

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

    def get_friend_suggesion(self):
        """
        Get 10 friends of friends who are not already friends.
        """
        query1 = """
        MATCH (user:User {user_id: $user_id})
        MATCH (user)-[:FRIENDS_WITH]-(friend)-[:FRIENDS_WITH]-(suggested:User)
        WHERE NOT (user)-[:FRIENDS_WITH]-(suggested) 
        AND user <> suggested
        AND NOT (user)-[:SENT_REQUEST]-(:FriendRequest)-[:RECEIVED_REQUEST]-(suggested)
        WITH DISTINCT suggested, user
        OPTIONAL MATCH (user)-[:SENT_REQUEST]-(:FriendRequest)-[:RECEIVED_REQUEST]-(suggested)
        OPTIONAL MATCH (user)-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(suggested)
        WITH 
        suggested.user_id AS user_id, 
        suggested.full_name AS full_name, 
        COLLECT(DISTINCT mutual)[..2] AS mutual_friends_list, 
        COLLECT(DISTINCT mutual.full_name)[..10] AS mutual_friends_name_list,
        COUNT(mutual) AS mutual_friends_count, 
        CASE WHEN (user)-[:SENT_REQUEST]-(:FriendRequest)-[:RECEIVED_REQUEST]-(suggested) THEN true ELSE false END AS sent_request,
        rand() AS random_order
        RETURN 
        user_id, 
        full_name, 
        sent_request,
        mutual_friends_count, 
        mutual_friends_list, 
        mutual_friends_name_list
        ORDER BY random_order
        LIMIT 200
        """

        max_friends_suggestions_count = 200

        parameters = {"user_id": self.user_id}

        results, _ = db.cypher_query(query1, parameters)

        friend_suggestions = []

        if not results:
            return self.get_random_user_list()

        for record in results:
            friend_obj = {
                "id": str(uuid.UUID(str(record[0]))),
                "full_name": record[1],
                "is_friend": False,
                "sent_request": record[2],
                "received_request": False,
                "mutual_friends": record[3],
                "mutual_friends_list": [],
                "mutual_friends_name_list": record[5],
            }

            for friend in record[4]:
                friend = User.inflate(friend)
                friend_obj["mutual_friends_list"].append(
                    {
                        "id": str(uuid.UUID(str(friend.user_id))),
                        "full_name": friend.full_name,
                    }
                )
            
            friend_suggestions.append(friend_obj)
        
        if len(friend_suggestions) < max_friends_suggestions_count:
            random_users = self.get_random_user_list(
                max_friends_suggestions_count - len(friend_suggestions)
            )
            friend_suggestions.extend(random_users)

        return friend_suggestions

    def get_random_user_list(self, count):
        """
        Get a list of random users.
        """
        query = """
        MATCH (user:User)
        WITH user, rand() AS random_order
        ORDER BY random_order
        RETURN user
        LIMIT $count
        """

        parameters = {"user_id": self.user_id, "count": count}

        results, _ = db.cypher_query(query, parameters)

        random_users = []

        for record in results:
            user = User.inflate(record[0])
            random_users.append(
                {
                    "id": str(uuid.UUID(str(user.user_id))),
                    "full_name": user.full_name,
                    "is_friend": False,
                    "sent_request": False,
                    "received_request": False,
                    "mutual_friends": 0,
                    "mutual_friends_list": [],
                    "mutual_friends_name_list": [],
                }
            )

        return random_users


    def __str__(self):
        return f"{self.full_name} - {self.user_id}"