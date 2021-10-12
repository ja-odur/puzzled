from django.contrib.auth import get_user_model
from django.db import models
from backend.gem.models import Gem


class PokerPlayerManager(models.Manager):
    def get_or_create(self, user_id):
        try:
            player = self.model.objects.get(user__id=user_id)

        except self.model.DoesNotExist:
            user = get_user_model().objects.get(id=user_id)
            gem = Gem.objects.get(user__id=user_id)
            player = self.model(gem=gem, user=user)
            player.save()

        return player
