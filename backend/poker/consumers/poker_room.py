from ..poker_game import poker_room_streams
from ..serializers import PokerRoomSerializer
from ..types import PokerRoomType


class PokerRoomConsumer:
    def __init__(self):
        self.stream = None

    def subscribe(self, room_id):
        self.stream = poker_room_streams.poll_stream(room_id, self.serialize)
        return self.stream

    def unsubscribe(self):
        return

    def serialize(self):
        return

    def deserialize(self):
        return

    def type(self):
        return PokerRoomType
