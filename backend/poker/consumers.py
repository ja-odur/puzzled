from .poker_game import poker_room_streams
from .serializers import PokerRoomSerializer

class PokerRoomConsumer:
    def subscribe(self, room_id):
        poker_room_streams.poll_stream(room_id, self.serialize)

    def unsubscribe(self):
        return

    def serialize(self):
        PokerRoomSerializer

    def deserialize(self):
        return

    def type(self):
        return PokerRoomType
