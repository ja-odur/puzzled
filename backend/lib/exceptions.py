class FieldValidationError(Exception):
    def __init__(self, message, field, params, code='required'):
        super().__init__(message)
        self.field = field
        self.message = message
        self.params = params
        self.code = code


class GraphQLValidationError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
