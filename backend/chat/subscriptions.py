import graphene
from backend.lib.signal_handlers.m2m_events import POST_ADD

from .models import ChatChannel
from .model_types import ChatChannelModelType


class ChatChannelUpdatedType(graphene.ObjectType):
    chat_channel_updated = graphene.Field(ChatChannelModelType, id=graphene.ID())

    def resolve_chat_channel_updated(root, info, id):
        return root.filter(
            lambda event: event.operation == POST_ADD
            and isinstance(event.instance, ChatChannel)
            and event.instance.pk == int(id)
        ).map(lambda event: event.instance)
