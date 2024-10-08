import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=500)

    def __str__(self):
        return self.email


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
