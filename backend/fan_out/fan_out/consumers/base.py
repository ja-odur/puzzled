import graphene
from backend.fan_out.fan_out.interfaces import AbstractConsumer
from .poker import PokerRoomConsumer


class FanOutConsumers(dict):
    def __init__(self, **consumers):
        super().__init__()
        self.consumers = consumers
        self.types = [consumer.type for consumer in self.consumers.values()]

    @property
    def consumers(self):
        return self._consumers

    @consumers.setter
    def consumers(self, consumers):
        for key, consumer in consumers.items():
            if not issubclass(consumer, AbstractConsumer):
                raise Exception(
                    f'{key} consumer must inherit from {AbstractConsumer.__name__}'
                )
            self[key] = consumer

        self._consumers = consumers


fan_out_consumers = FanOutConsumers(poker_room=PokerRoomConsumer())


class FanOutConsumerTypes(graphene.Union):
    class Meta:
        types = fan_out_consumers.types

