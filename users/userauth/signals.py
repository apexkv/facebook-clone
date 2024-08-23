from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from userauth.models import BaseUser


@receiver(post_delete, sender=BaseUser)
def delete_profile_pic_on_delete(sender: BaseUser, instance: BaseUser, **kwargs):
    if instance.profile_pic:
        instance.profile_pic.delete(save=False)


@receiver(pre_save, sender=BaseUser)
def delete_old_profile_pic_on_update(sender: BaseUser, instance: BaseUser, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).profile_pic
    except sender.DoesNotExist:
        return False

    new_file = instance.profile_pic
    if not old_file == new_file:
        old_file.delete(save=False)
