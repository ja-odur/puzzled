from graphene_django import DjangoObjectType
from backend.poker.models import PokerRoom
from backend.lib.types import NoneConvertedEnumDjangoObjectType


class PokerRoomType(NoneConvertedEnumDjangoObjectType):

    class Meta:
        model = PokerRoom
