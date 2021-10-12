import graphene
from graphene_django import DjangoObjectType
from backend.lib.base import BaseMutation
from backend.lib.types import Error
from backend.lib.decorators.permissions import is_authenticated
from .models import PokerPlayer
from .poker_game import PokerGame


class PokerPlayerType(DjangoObjectType):

    class Meta:
        model = PokerPlayer


class CreatePokerRoom(BaseMutation):
    room_id = graphene.String()
    poker_type = graphene.String()
    small_blind = graphene.Int()
    big_blind = graphene.Int()
    players = graphene.List(graphene.NonNull(graphene.String), required=False)
    name = graphene.String(required=False)
    from_deck = graphene.List(graphene.NonNull(graphene.List(graphene.String)))
    deck_size = graphene.Int()
    dealer = graphene.Int(required=False)

    class Meta:
        description = 'Create Poker room'
        error_type_class = Error
        error_type_field = "create_poker_room_errors"

    class Arguments:
        poker_type = graphene.String(required=True)
        small_blind = graphene.Int(required=True)
        big_blind = graphene.Int(required=True)
        players = graphene.List(graphene.NonNull(graphene.String), required=False)
        name = graphene.String(required=False)
        from_deck = graphene.List(graphene.NonNull(graphene.List(graphene.String)), required=False)
        deck_size = graphene.Int(required=False)
        dealer = graphene.Int(required=False)

    @classmethod
    @is_authenticated
    def perform_mutation(
            cls,
            info,
            poker_type,
            small_blind,
            big_blind,
            players=(),
            name=None,
            from_deck=None,
            deck_size=1,
            dealer=None):

        new_game = PokerGame(
            poker_type=poker_type,
            small_blind=small_blind,
            big_blind=big_blind,
            players=players,
            name=name,
            from_deck=from_deck,
            dealer=None
        )

        return cls(
            room_id=new_game.room.poker_room,
            poker_type=poker_type,
            small_blind=small_blind,
            big_blind=big_blind,
            players=players,
            name=name,
            from_deck=from_deck,
            deck_size=deck_size,
            dealer=dealer
        )


class AddPokerPlayer(BaseMutation):
    player = graphene.Field(PokerPlayerType)

    class Meta:
        description = 'Add player to room'
        error_type_class = Error
        error_type_field = "add_player_to_room_errors"

    class Arguments:
        room_id = graphene.String(required=True)
        user_id = graphene.String(required=True)

    @classmethod
    @is_authenticated
    def perform_mutation(cls, info, room_id, user_id):

        player = PokerGame.add_player(room_id=room_id, user_id=user_id)

        return cls(player=player)
