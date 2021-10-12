from django.db import models


class PokerRoomManager(models.Manager):
    def add_player(self, room_id, user_id):
        from backend.poker.models import PokerPlayer

        try:
            room = self.get(id=room_id)
        except self.model.DoesNotExist as exc:
            raise exc

        player = PokerPlayer.objects.get_or_create(user_id=user_id)

        room.players.add(player)

        return player
