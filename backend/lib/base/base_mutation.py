import graphene
from graphene.types.mutation import MutationOptions
from graphene.utils.props import props
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from backend.lib.exceptions import FieldValidationError, GraphQLValidationError
from backend.lib.types import Error
from backend.lib.utils import get_error_code_from_error, print_exception, snake_to_camel_case

EXCLUDED_EXCEPTIONS = [ObjectDoesNotExist]


def get_error_fields(error_type_class, error_type_field):
    return {
        error_type_field: graphene.Field(
            graphene.List(
                graphene.NonNull(error_type_class),
                description="List of errors that occurred while executing the mutation.",
            ),
            default_value=[],
        )
    }


def validation_error_to_error_type(validation_error):
    """Convert a ValidationError into a list of Error types."""

    for exc in EXCLUDED_EXCEPTIONS:
        if isinstance(validation_error, exc):
            raise validation_error

    if not isinstance(validation_error, FieldValidationError):
        print_exception()

        raise Exception(
            f'All ValidationError Exceptions must inherit from {FieldValidationError.__name__}') from validation_error

    return [
        (
            Error(field=validation_error.field, message=validation_error.message, code=validation_error.code),
            get_error_code_from_error(validation_error),
            validation_error.params
        )
    ]


class BaseMutation(graphene.Mutation):
    errors = graphene.List(
        graphene.NonNull(Error),
        description="List of errors that occurred while executing the mutation.",
    )

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
            cls,
            description=None,
            _meta=None,
            error_type_class=None,
            error_type_field=None,
            model=None,
            unique_together=(),
            **options):
        if not _meta:
            _meta = MutationOptions(cls)

        if not description:
            raise ImproperlyConfigured("No description provided in Meta")

        validators_class = getattr(cls, "Validators", None)

        if validators_class:
            validators = props(validators_class)
        else:
            validators = {}

        if unique_together:
            if not model or model is None:
                raise ImproperlyConfigured('No model found in the Meta class')

        _meta.error_type_class = error_type_class
        _meta.error_type_field = error_type_field
        _meta.validators = validators
        _meta.unique_together = unique_together
        _meta.model = model
        super().__init_subclass_with_meta__(description=description, _meta=_meta, **options)

        if error_type_class and error_type_field:
            cls._meta.fields.update(get_error_fields(error_type_class, error_type_field))

    @classmethod
    def mutate(cls, root, info, **data):
        cls.run_validation(**data)

        try:
            response = cls.perform_mutation(info, **data)
            if response.errors is None:
                response.errors = []
            return response
        except Exception as e:
            return cls.handle_errors(e)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass

    @classmethod
    def run_validation(cls, **input_data):
        errors = []
        for key, validator in cls._meta.validators.items():
            value = input_data.get(key)
            if value:
                try:
                    validator(value)
                except FieldValidationError as e:
                    errors.extend(validation_error_to_error_type(e))
                except Exception as e:
                    errors.extend(
                        [
                            (
                                Error(field=key, message=str(e), code='Invalid'),
                                'Invalid',
                                value
                            )
                        ]
                    )

        errors.extend(cls.run_model_unique_checks(**input_data))
        if errors:
            cls.handle_typed_errors(errors)

    @classmethod
    def run_model_unique_checks(cls, **input_data):
        errors = []
        filters = {
            key: value for key, value in input_data.items() if key in cls._meta.unique_together
        }

        if cls._meta.model and cls._meta.model.objects.filter(**filters):

            for field in cls._meta.unique_together:
                errors.extend([
                    (
                        Error(
                            field=field,
                            message=f'{cls._meta.model.__name__} with {cls._meta.unique_together} already exists',
                            code='Invalid'
                        ),
                        'Invalid',
                        input_data.get(field)
                    )

                ])

        return errors

    @classmethod
    def handle_errors(cls, error, **extra):
        errors = validation_error_to_error_type(error)
        return cls.handle_typed_errors(errors, **extra)

    @classmethod
    def handle_typed_errors(cls, errors: list, **extra):
        """Return class instance with errors."""

        if cls._meta.error_type_class is not None and cls._meta.error_type_field is not None:
            typed_errors = [
                cls._meta.error_type_class(field=e.field, message=e.message, code=code)
                for e, code, _params in errors
            ]
            extra.update({cls._meta.error_type_field: typed_errors})

            formatted_errors = [dict(field=snake_to_camel_case(error.field),
                                     message=error.message, code=error.code) for error in typed_errors]

            raise GraphQLValidationError('Validation failed', formatted_errors)
        return cls(errors=[e[0] for e in errors], **extra)
