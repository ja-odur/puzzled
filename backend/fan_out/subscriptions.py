import graphene
from rx import Observable
from .fan_out.consumers import fan_out_consumers, FanOutConsumerTypes
from backend.lib.signal_handlers.m2m_events import POST_ADD


class FanOutSubscribe(graphene.ObjectType):
    consumer = graphene.Field(FanOutConsumerTypes, consumer=graphene.String(), identifier=graphene.ID())

    def resolve_consumer(root, info, consumer, identifier):
        consumer = fan_out_consumers.get(consumer)

        if not consumer:
            raise

        return consumer.subscribe(identifier)

    #
    # chat_channel_updated = graphene.Field(ChatChannelModelType, id=graphene.ID())
    #
    # def resolve_chat_channel_updated(root, info, id):
    #     return root.filter(
    #         lambda event:
    #             event.operation == POST_ADD and
    #             isinstance(event.instance, ChatChannel) and
    #             event.instance.pk == int(id)
    #     ).map(lambda event: event.instance)

