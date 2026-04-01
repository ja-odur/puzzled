import graphene
from graphene_django import DjangoObjectType
from backend.lib.decorators.permissions import is_authenticated
from backend.lib.exceptions import FieldValidationError
from .models import Gem


class GemModelType(DjangoObjectType):
    class Meta:
        model = Gem


class GemQuery(graphene.ObjectType):
    gem = graphene.Field(GemModelType, user=graphene.String())

    @is_authenticated
    def resolve_gem(self, info, user):
        gem = Gem.objects.get(user=user)

        if gem.user == info.context.user:
            return gem

        raise FieldValidationError(
            'You do not have the required permission to view this field',
            field=None,
            params=None,
            code='Invalid',
        )
