import graphene
from .mutations import (
    AddMessage,
    EditMessage,
    CreateOrGetDirectChatChannelMutation,
    CreateOrGetMultiUserChatChannelMutation,
)
from .subscriptions import ChatChannelUpdatedType


class ChatSubscriptions(ChatChannelUpdatedType, graphene.ObjectType):
    pass


class ChatMutations(graphene.ObjectType):
    create_or_get_direct_chat = CreateOrGetDirectChatChannelMutation.Field()
    create_or_get_multi_user_chat = CreateOrGetMultiUserChatChannelMutation.Field()
    add_message = AddMessage.Field()
    edit_message = EditMessage.Field()
