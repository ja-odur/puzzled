import graphene
from .types import PokerRoomType


class PokerRoomSubscription(graphene.ObjectType):
    consumer = graphene.Field(PokerRoomType)

    def resolve_consumer(root, info):
        pass

