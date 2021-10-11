import graphene
from .mutations import AddPokerPlayer, CreatePokerRoom
from .subscriptions import PokerRoomSubscription


class PokerMutations(graphene.ObjectType):
    add_poker_player = AddPokerPlayer.Field()
    create_poker_room = CreatePokerRoom.Field()


class PokerSubscriptions(graphene.ObjectType):
    poker_room = graphene.Field(PokerRoomSubscription)
