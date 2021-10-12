import graphene
# from .subscriptions import FanOutSubscribe
from .subscriptions import FanOutConsumerTypes, fan_out_consumers


class FanOutSubscriptions(graphene.ObjectType):
    consumer = graphene.Field(fan_out_consumers.types[0])
