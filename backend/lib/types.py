import graphene
from graphene_django import DjangoObjectType
from graphene.types.mutation import MutationOptions
from .validators import validate_email, url_validator


class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")
    code = graphene.String()

    class Meta:
        description = "Represents an error in the input of a mutation."


class EmailField(graphene.String):

    @staticmethod
    def parse_value(value):

        if not validate_email(value):
            return None
        return super().parse_value(value)

    @staticmethod
    def parse_literal(ast):
        if validate_email(ast.value):
            return ast.value


class URLField(graphene.String):
    @staticmethod
    def parse_value(value):
        try:
            url_validator(value)
        except ValueError:
            return None
        return super().parse_value(value)

    @staticmethod
    def parse_literal(ast):
        try:
            url_validator(ast.value)
        except ValueError:
            pass
        else:
            return ast.value


class NoneConvertedEnumDjangoObjectType(DjangoObjectType):
    """DjangoObjectType with convert_choices_to_enum option disabled (set to False)
       For more info check https://github.com/graphql-python/graphene-django/pull/674
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, convert_choices_to_enum=False, _meta=None, **options):
        if not _meta:
            _meta = MutationOptions(cls)

        if convert_choices_to_enum:
            raise Exception(f'Invalid "convert_choices_to_enum" value of "{convert_choices_to_enum}". '
                            f'Expected value is "False" otherwise simply inherit from "DjangoObjectType"')

        super().__init_subclass_with_meta__(convert_choices_to_enum=convert_choices_to_enum, _meta=_meta, **options)
