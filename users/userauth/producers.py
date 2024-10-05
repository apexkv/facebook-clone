from apexmq.producers import on_model_create, on_model_update, on_model_delete
from .models import BaseUser


on_model_create(BaseUser, "broadcast")
on_model_update(BaseUser, "broadcast")
on_model_delete(BaseUser, "broadcast")
