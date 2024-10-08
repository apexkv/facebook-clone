import uuid
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from users.producers import publish


def new_file_name(instance, filename):
    ext = filename.split(".")[-1]
    return f"{instance.id}.{ext}"


class BaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = None
    last_name = None
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)

    profile_pic = models.ImageField(null=True, blank=True, upload_to=new_file_name)

    def update_lastlogin(self):
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    def __str__(self) -> str:
        return self.email


@receiver(signals.post_save, sender=BaseUser)
def handle_on_user_create_or_update(sender, instance, created, **kwargs):
    action_type = "user.created" if created else "user.updated"
    publish(action_type, {"id": str(instance.id), "email": instance.email}, "broadcast")
