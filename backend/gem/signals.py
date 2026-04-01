from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import Gem


def post_save_gem_handler(sender, instance, *args, created=False, **kwargs):

    if created:
        Gem(user=instance).save()


post_save.connect(
    post_save_gem_handler,
    sender=get_user_model(),
    dispatch_uid=f'{get_user_model().__class__.__name__}_gem_signal',
)
