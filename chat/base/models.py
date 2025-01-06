import uuid
from django.db import models
from django.utils import timezone


class User(models.Model):
    """
    User model to store basic user information
    """
    id = models.UUIDField(primary_key=True, editable=False, db_index=True)
    full_name = models.CharField(max_length=500, db_index=True)
    is_online = models.BooleanField(default=False, db_index=True)
    last_seen = models.DateTimeField(null=True, db_index=True)

    def user_online(self):
        self.is_online = True
        self.save()
        print(f"[online] {self}")
    
    def user_offline(self):
        self.is_online = False
        self.save()
        self.set_last_seen()
        print(f"[offline] {self}")
    
    def set_last_seen(self):
        self.last_seen = timezone.now()
        self.save()

    def __str__(self):
        return self.full_name


class Room(models.Model):
    """
    Room model to store room information: friends, last message time
    """
    id = models.UUIDField(primary_key=True, editable=False, db_index=True, default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name="users", db_index=True)
    last_message_at = models.DateTimeField(null=True, db_index=True)

    def __str__(self):
        return f"{self.users.all()}"


class Message(models.Model):
    """
    Message model to store message information: room, user, content, created_at, is_read
    """
    id = models.UUIDField(primary_key=True, editable=False, db_index=True, default=uuid.uuid4)

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages", db_index=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    is_read = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.content
