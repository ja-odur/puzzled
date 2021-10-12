from io import BytesIO
from rest_framework.serializers import ModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import PokerRoom, PokerHand


class PokerRoomSerializer(ModelSerializer):
    class Meta:
        model = PokerRoom

    def to_json(self):
        return JSONRenderer().render(self.data)

    @classmethod
    def deserialize(cls, json_data):
        return cls(data=JSONParser().parse(BytesIO(json_data)))
