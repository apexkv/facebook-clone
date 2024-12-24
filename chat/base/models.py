import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_index=True)
    full_name = models.CharField(max_length=500, db_index=True)
    is_online = models.BooleanField(default=False, db_index=True)

    def user_online(self):
        self.is_online = True
        self.save()
        print(f"[online] {self}")
    
    def user_offline(self):
        self.is_online = False
        self.save()
        print(f"[offline] {self}")

    def __str__(self):
        return self.full_name


class Friendship(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_index=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", db_index=True)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend", db_index=True)
    room = models.UUIDField(db_index=True, default=uuid.uuid4)

    def __str__(self):
        return f"{self.user} - {self.friend}"
    


class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_index=True, default=uuid.uuid4)

    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_from", db_index=True)
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to", db_index=True)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
