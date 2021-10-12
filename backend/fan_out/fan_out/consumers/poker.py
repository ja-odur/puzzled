from backend.poker.poker_game import poker_room_streams
# from ..types import PokerRoomType
from backend.lib.types import NoneConvertedEnumDjangoObjectType
from backend.poker.models import PokerRoom
# from ..types import PokerRoomType as P
# import graphene
#
# from functools import lru_cache
#
# graphene.Enum.from_enum = lru_cache(maxsize=None)(graphene.Enum.from_enum)

class PokerRoomType(NoneConvertedEnumDjangoObjectType):

    class Meta:
        model = PokerRoom


class PokerRoomConsumer:
    def __init__(self):
        self.stream = None

    def subscribe(self, room_id):
        self.stream = poker_room_streams.poll_stream(room_id, self.serialize)
        return

    def unsubscribe(self):
        return

    def serialize(self):
        return

    def deserialize(self):
        return

    def type(self):
        return PokerRoomType

# class PokerRoomConsumer:
#     def subscribe(self, room_id):
#         poker_room_streams.poll_stream(room_id, self.serialize)
#
#     def unsubscribe(self):
#         return
#
#     def serialize(self):
#         return
#
#     def deserialize(self):
#         return
#
#     @property
#     def type(self):
#         # return P
#         return PokerRoomType
