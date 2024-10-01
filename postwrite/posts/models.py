from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
